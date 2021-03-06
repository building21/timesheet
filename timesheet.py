from flask import Flask, render_template, request, url_for, redirect
from wtforms import Form, validators, TextField, IntegerField, DecimalField, SelectField, TimeField, ValidationError
from wtforms.widgets import Input
from flask_wtf import FlaskForm, RecaptchaField
from pdf_annotate import PdfAnnotator, Location, Appearance
import time, datetime, random, string, os, pytz, constants


app = Flask(__name__)
app.config.from_envvar('FLASK_APP_SETTINGS')

class OutTimeValidator(object):
	"""
	Compares the in and out times to ensure the out time is after the in time.
	Checks for a in time value.
	:param in_time_field:
		The name of the in_time field to check and compare to.
	"""

	def __init__(self, in_time_field):
		self.in_time_field = in_time_field

	def __call__(self, form, field):
		other = form[self.in_time_field]

		if other.data is None:
			message = "Must submit an in time for the day"
			raise ValidationError(message)

		in_time = other.data
		out_time = field.data

		if out_time < in_time:
			message = "Out time must be after the in time for the day"
			raise ValidationError(message)

class InTimeValidator(object):
	"""
	Checks for an out time value.
	:param out_time_field:
		The name of the out_time field to check.
	"""

	def __init__(self, out_time_field):
		self.out_time_field = out_time_field

	def __call__(self, form, field):
		if form[self.out_time_field].data is None:
			message = "Must submit an out time for the day"
			raise ValidationError(message)		


class TimesheetForm(FlaskForm):
	# def out_time_validator(in_time):
	# 	message = "Out time must be after in time!"

	# 	def _out_time_validator(form, field):
	# 		print(in_time)
	# 		out_time = time.strptime(field, '%H:%M')

	name = TextField('Name:', validators=[validators.required()])
	mcgill_id = IntegerField('McGill ID:', validators=[validators.required(), validators.NumberRange(min=260000000, max=260999999, message="Are you sure that looks like a McGill ID number?")])
	hourly_rate = DecimalField('Hourly rate:', validators=[validators.required()])
	fund_number = IntegerField('Fund number:', validators=[validators.optional()])
	timesheet_template = SelectField('Timesheet template:', validators=[validators.required()], default='1',
		choices=constants.timesheet_template_choices)

	default_date = datetime.datetime.now()
	default_date_montreal = pytz.timezone('America/Toronto').localize(default_date)

	week_of_year = SelectField('Week of:', validators=[validators.required()], default=str(default_date_montreal.year),
		choices=constants.week_of_year_choices)
	week_of_month = SelectField('Week of:', validators=[validators.required()], default=str(default_date_montreal.month),
		choices=constants.week_of_month_choices)
	week_of_day = SelectField('Week of:', validators=[validators.required()], default=str(default_date_montreal.day),
		choices=constants.week_of_day_choices)

	sunday_in = TimeField(validators=[validators.optional(), InTimeValidator('sunday_out')], widget=Input(input_type='time'))
	sunday_out = TimeField(validators=[validators.optional(), OutTimeValidator('sunday_in')], widget=Input(input_type='time'))
	monday_in = TimeField(validators=[validators.optional(), InTimeValidator('monday_out')], widget=Input(input_type='time'))
	monday_out = TimeField(validators=[validators.optional(), OutTimeValidator('monday_in')], widget=Input(input_type='time'))
	tuesday_in = TimeField(validators=[validators.optional(), InTimeValidator('tuesday_out')], widget=Input(input_type='time'))
	tuesday_out = TimeField(validators=[validators.optional(), OutTimeValidator('tuesday_in')], widget=Input(input_type='time'))
	wednesday_in = TimeField(validators=[validators.optional(), InTimeValidator('wednesday_out')], widget=Input(input_type='time'))
	wednesday_out = TimeField(validators=[validators.optional(), OutTimeValidator('wednesday_in')], widget=Input(input_type='time'))
	thursday_in = TimeField(validators=[validators.optional(), InTimeValidator('thursday_out')], widget=Input(input_type='time'))
	thursday_out = TimeField(validators=[validators.optional(), OutTimeValidator('thursday_in')], widget=Input(input_type='time'))
	friday_in = TimeField(validators=[validators.optional(), InTimeValidator('friday_out')], widget=Input(input_type='time'))
	friday_out = TimeField(validators=[validators.optional(), OutTimeValidator('friday_in')], widget=Input(input_type='time'))
	saturday_in = TimeField(validators=[validators.optional(), InTimeValidator('saturday_out')], widget=Input(input_type='time'))
	saturday_out = TimeField(validators=[validators.optional(), OutTimeValidator('saturday_in')], widget=Input(input_type='time'))

	# recaptcha = RecaptchaField()

		
@app.route('/', methods=['GET', 'POST'])
def render_timesheet_form():
	form = TimesheetForm()

	if form.validate_on_submit():
		## render timesheet
		pdf = generate_timesheet(form)

		return redirect(url_for('static', filename=pdf))

	if form.sunday_in.errors or form.sunday_out.errors:
		print(form.sunday_in.errors, form.sunday_in.errors)
	return render_template('hello.html', form=form)

def generate_timesheet(form):
	# Setting default strings
	sunday_in = ''
	monday_in = ''
	tuesday_in = ''
	wednesday_in = ''
	thursday_in = ''
	friday_in = ''
	saturday_in = ''
	sunday_out = ''
	monday_out = ''
	tuesday_out = ''
	wednesday_out = ''
	thursday_out = ''
	friday_out = ''
	saturday_out = ''
	sunday_hours = ''
	monday_hours = ''
	tuesday_hours = ''
	wednesday_hours = ''
	thursday_hours = ''
	friday_hours = ''
	saturday_hours = ''
	fund = ''

	def calc_hours_worked(time_in, time_out):
		hours = datetime.datetime.combine(datetime.date.today(), time_out.data) - datetime.datetime.combine(datetime.date.today(), time_in.data)
		return round(hours.seconds/3600, 2)

	def next_saturday(d):
		if d.weekday() == 5:
			return d
		else:
			days_ahead = 5 - d.weekday()
			if days_ahead < 0:
				days_ahead += 7
			return d + datetime.timedelta(days_ahead)

	def previous_sunday(d):
		if d.weekday() == 6:
			return d
		else:
			days_behind = - d.weekday() - 1
			return d + datetime.timedelta(days_behind)

	name = form['name'].data
	mcgill_id = form['mcgill_id'].data
	hourly_rate = round(float(form['hourly_rate'].data),2)
	if form['fund_number'].data is not None:
		fund = form['fund_number'].data

	week = datetime.date(int(form['week_of_year'].data), int(form['week_of_month'].data), int(form['week_of_day'].data))
	# find the closest past sunday
	week_start = previous_sunday(week)
	# find the closest future saturday
	week_end = next_saturday(week)

	total_hours = 0
	if form['sunday_in'].data is not None and form['sunday_out'].data is not None: 
		sunday_in = form['sunday_in'].data.strftime('%H:%M')
		sunday_out = form['sunday_out'].data.strftime('%H:%M')
		sunday_hours = calc_hours_worked(form['sunday_in'], form['sunday_out'])
		total_hours += sunday_hours
	if form['monday_in'].data is not None and form['monday_out'].data is not None: 
		monday_in = form['monday_in'].data.strftime('%H:%M')
		monday_out = form['monday_out'].data.strftime('%H:%M')
		monday_hours = calc_hours_worked(form['monday_in'], form['monday_out'])
		total_hours += monday_hours
	if form['tuesday_in'].data is not None and form['tuesday_out'].data is not None: 
		tuesday_in = form['tuesday_in'].data.strftime('%H:%M')
		tuesday_out = form['tuesday_out'].data.strftime('%H:%M')
		tuesday_hours = calc_hours_worked(form['tuesday_in'], form['tuesday_out'])
		total_hours += tuesday_hours
	if form['wednesday_in'].data is not None and form['wednesday_out'].data is not None: 
		wednesday_in = form['wednesday_in'].data.strftime('%H:%M')
		wednesday_out = form['wednesday_out'].data.strftime('%H:%M')
		wednesday_hours = calc_hours_worked(form['wednesday_in'], form['wednesday_out'])
		total_hours += wednesday_hours
	if form['thursday_in'].data is not None and form['thursday_out'].data is not None: 
		thursday_in = form['thursday_in'].data.strftime('%H:%M')
		thursday_out = form['thursday_out'].data.strftime('%H:%M')
		thursday_hours = calc_hours_worked(form['thursday_in'], form['thursday_out'])
		total_hours += thursday_hours
	if form['friday_in'].data is not None and form['friday_out'].data is not None: 
		friday_in = form['friday_in'].data.strftime('%H:%M')
		friday_out = form['friday_out'].data.strftime('%H:%M')
		friday_hours = calc_hours_worked(form['friday_in'], form['friday_out'])
		total_hours += friday_hours
	if form['saturday_in'].data is not None and form['saturday_out'].data is not None: 
		saturday_in = form['saturday_in'].data.strftime('%H:%M')
		saturday_out = form['saturday_out'].data.strftime('%H:%M')
		saturday_hours = calc_hours_worked(form['saturday_in'], form['saturday_out'])
		total_hours += saturday_hours

	total_money = round(total_hours * hourly_rate,2)

	if form['timesheet_template'].data == '1':
		base_timesheet = 'academic_casual_timesheet_-_2017_0.pdf'
		annotations = constants.annotations_academic_casual_timesheet
		personal_data = constants.personal_data_academic_casual_timesheet
	else:
		base_timesheet = 'admin_support_staff_casual_employee_timesheet_-_2017.pdf'
		annotations = constants.annotations_admin_support_staff_casual_employee_timesheet
		personal_data = constants.personal_data_admin_support_staff_casual_employee_timesheet


	pdf_out_dir = 'pdf/'
	out_file = form['name'].data + ' ' + week_start.strftime('%d %b %Y') + '.pdf'
	# out_file = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) + '.pdf'
	out_path = pdf_out_dir + out_file

	department = 'Building 21'
	signature_date = datetime.date.today()
	

	timesheet = PdfAnnotator(base_timesheet)
	
	for annotation in annotations:
		x1 = annotation[1]
		y1 = annotation[2]
		x2 = x1 + annotation[3]
		y2 = y1 + annotation[4]
		timesheet.add_annotation(
			'text',
			Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
			Appearance(content=str(eval(annotation[0])), fill=(0,0,0), text_baseline='bottom'),
		)

	for annotation in personal_data:
		x1 = annotation[1]
		y1 = annotation[2]
		x2 = x1 + annotation[3]
		y2 = y1 + annotation[4]
		timesheet.add_annotation(
			'text',
			Location(x1=x1, y1=y1, x2=x2, y2=y2, page=0),
			Appearance(content=str(eval(annotation[0])), fill=(0,0,0), text_baseline='middle', text_align='center'),
		)
	
	timesheet.write('static/' + out_path)

	return out_path

