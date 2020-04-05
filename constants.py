timesheet_template_choices = [('1', 'Academic Casual'),
	('2', 'Administrative & support staff (casual)')]

week_of_year_choices = [('2020', '2020'), ('2021', '2021')]
week_of_month_choices = [('1', 'Jan'),
	('2', 'Feb'),
	('3', 'Mar'),
	('4', 'Apr'),
	('5', 'May'),
	('6', 'Jun'),
	('7', 'Jul'),
	('8', 'Aug'),
	('9', 'Sep'),
	('10', 'Oct'),
	('11', 'Nov'),
	('12', 'Dec')]
week_of_day_choices = [('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
	('6', '6'),
	('7', '7'),
	('8', '8'),
	('9', '9'),
	('10', '10'),
	('11', '11'),
	('12', '12'),
	('13', '13'),
	('14', '14'),
	('15', '15'),
	('16', '16'),
	('17', '17'),
	('18', '18'),
	('19', '19'),
	('20', '20'),
	('21', '21'),
	('22', '22'),
	('23', '23'),
	('24', '24'),
	('25', '25'),
	('26', '26'),
	('27', '27'),
	('28', '28'),
	('29', '29'),
	('30', '30'),
	('31', '31')]

annotations_academic_casual_timesheet = [
	('name', 160, 667, 175, 20),
	('mcgill_id', 395, 667, 100, 20),
	('department', 150, 630, 100, 20),
	('week_start', 210, 592, 90, 20),
	('week_end', 390, 592, 90, 20),
	('signature_date', 250, 321, 90, 20),
	('fund', 70, 220, 90, 20)
]

personal_data_academic_casual_timesheet = [
	('sunday_in', 221, 512, 54, 20),
	('sunday_out', 276, 512, 42, 20),
	('sunday_hours', 362, 512, 55, 20),
	
	('monday_in', 221, 491, 54, 20),
	('monday_out', 276, 491, 42, 20),
	('monday_hours', 362, 491, 55, 20),
	
	('tuesday_in', 221, 470, 54, 20),
	('tuesday_out', 276, 470, 42, 20),
	('tuesday_hours', 362, 470, 55, 20),
	
	('wednesday_in', 221, 448, 54, 20),
	('wednesday_out', 276, 448, 42, 20),
	('wednesday_hours', 362, 448, 55, 20),
	
	('thursday_in', 221, 427, 54, 20),
	('thursday_out', 276, 427, 42, 20),
	('thursday_hours', 362, 427, 55, 20),
	
	('friday_in', 221, 406, 54, 20),
	('friday_out', 276, 406, 42, 20),
	('friday_hours', 362, 406, 55, 20),
	
	('saturday_in', 221, 385, 54, 20),
	('saturday_in', 276, 385, 42, 20),
	('saturday_hours', 362, 385, 55, 20),

	('total_hours', 362, 363, 55, 20),
	('hourly_rate', 362, 342, 55, 20),
	('total_money', 362, 321, 55, 20),
]

annotations_admin_support_staff_casual_employee_timesheet = [
	('name', 160, 667, 175, 20),
	('mcgill_id', 395, 667, 100, 20),
	('department', 150, 630, 100, 20),
	('week_start', 210, 592, 90, 20),
	('week_end', 390, 592, 90, 20),
	('signature_date', 250, 321, 90, 20),
	('fund', 70, 220, 90, 20)
]

personal_data_admin_support_staff_casual_employee_timesheet = [
	('sunday_in', 221, 512, 43, 20),
	('sunday_out', 265, 512, 42, 20),
	('sunday_hours', 350, 512, 55, 20),
	
	('monday_in', 221, 491, 43, 20),
	('monday_out', 265, 491, 42, 20),
	('monday_hours', 350, 491, 55, 20),
	
	('tuesday_in', 221, 470, 43, 20),
	('tuesday_out', 265, 470, 42, 20),
	('tuesday_hours', 350, 470, 55, 20),
	
	('wednesday_in', 221, 448, 43, 20),
	('wednesday_out', 265, 448, 42, 20),
	('wednesday_hours', 350, 448, 55, 20),
	
	('thursday_in', 221, 427, 43, 20),
	('thursday_out', 265, 427, 42, 20),
	('thursday_hours', 350, 427, 55, 20),
	
	('friday_in', 221, 406, 43, 20),
	('friday_out', 265, 406, 42, 20),
	('friday_hours', 350, 406, 55, 20),
	
	('saturday_in', 221, 385, 43, 20),
	('saturday_in', 265, 385, 42, 20),
	('saturday_hours', 350, 385, 55, 20),

	('total_hours', 350, 363, 55, 20),
	('hourly_rate', 350, 342, 55, 20),
	('total_money', 350, 321, 55, 20),
]