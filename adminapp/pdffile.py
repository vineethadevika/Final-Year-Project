from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from .models import Examallotment
from reportlab.platypus import PageBreak
from io import BytesIO
from reportlab.lib.units import mm
from django.http import HttpResponse


def generate_examallotment_pdf(request):
    # Query data from the Examallotment table
    examallotments = Examallotment.objects.all()

    # Create a buffer to store PDF in memory
    buffer = BytesIO()

    # Create a PDF document with slightly adjusted margins
    pdf = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=72, bottomMargin=72)
    elements = []

    # Iterate through examallotments and group by department
    departments = sorted(set(examallotment.department for examallotment in examallotments))
    for department in departments:
        # Add page break for each department after the first one
        if elements:
            elements.append(PageBreak())

        # Add Aditya Engineering College centered
        elements.append(Paragraph("<b>ADITYA ENGINEERING COLLEGE</b>", getSampleStyleSheet()['Title']))
        elements.append(Spacer(1, 12)) 

        # Add Seating Arrangement heading centered
        elements.append(Paragraph("<b>SEATING ARRANGEMENT</b>", getSampleStyleSheet()['Title']))
        elements.append(Spacer(1, 12))  # Add some space after the heading

        # Collect starttime, endtime, and date from examallotment table for the current department
        department_examallotments = examallotments.filter(department=department)
        starttime = department_examallotments.first().starttime
        endtime = department_examallotments.first().endtime
        date = department_examallotments.first().date
        venue = "BGB"  # Venue information

        # Add exam timings header before the start time
        # Create a table for Exam Timings and Date on the same line

        # Define style for body text
        body_text_style = getSampleStyleSheet()['BodyText']

        # Create a table for Exam Timings and Date
        exam_timings_and_date = Table([
            [Paragraph("<b>Exam Timings:</b>", body_text_style), Spacer(1, 1), Paragraph("<b>Date:</b> " + str(date), body_text_style)]
        ], colWidths=[270, 100, 200])

        # Set style and alignment for the table
        exam_timings_and_date.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]))

        # Append the table to the elements list
        elements.append(exam_timings_and_date)



        elements.append(Spacer(1, 6))  # Adjust spacing after the header

        # Add starttime, endtime, date, and venue for the current department
        start_time = f"<b>Start Time:</b> {starttime}"
        end_time = f"<b>End Time:</b> {endtime}"
        # exam_date = f"<b>Date:</b> {date}"
        exam_venue = f"<b>Venue:</b> {venue}"
        elements.extend([
            Paragraph(start_time, getSampleStyleSheet()['BodyText']),
            Paragraph(end_time, getSampleStyleSheet()['BodyText']),
            # Paragraph(exam_date, getSampleStyleSheet()['BodyText']),
            Paragraph(exam_venue, getSampleStyleSheet()['BodyText']),
            Spacer(1, 18)  # Adjust spacing
        ])

        # Add department heading
        elements.append(Paragraph(f"<b>Department: {department}</b>", getSampleStyleSheet()['Title']))
        elements.append(Spacer(1, 12))  # Add some space after department heading

        # Create a dictionary to hold data for each room
        room_data = {}

        # Filter examallotments for the current department
        department_examallotments = examallotments.filter(department=department)

        # Iterate through examallotments for this department and group by room
        for examallotment in department_examallotments:
            key = examallotment.RoomNo
            if key not in room_data:
                room_data[key] = []
            room_data[key].append(examallotment)

        # Initialize serial number
        serial_no = 1

        # Create a list to hold combined data for all rooms in this department
        combined_data = [['S.No', 'Roll Numbers', 'Room No', 'Total']]

        # Iterate through room data
        for room, room_examallotments in room_data.items():
            # Initialize variables for roll number range and total count for this room
            roll_numbers = []
            total_count = len(room_examallotments)

            # Iterate through examallotments for this room
            for examallotment in room_examallotments:
                roll_numbers.append(examallotment.Student_Id)

            # Append combined data for this room to the list
            combined_data.append([
                serial_no,
                f"{min(roll_numbers)} to {max(roll_numbers)}",
                room,
                total_count
            ])

            # Increment serial number for the next entry
            serial_no += 1

        # Add table with left and right padding for all rooms in this department


        # Define the column widths
        col_widths = [150, 150, 150, 100]  # Adjust the widths as needed

        # Create the table
        table = Table(combined_data, colWidths=col_widths)

        # Define the table style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),        # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Center alignment for all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),     # Bold font for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 18),              # Padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),      # Alternate row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),         # Gridlines for all cells
            ('LEFTPADDING', (0, 0), (-1, -1), 6),                # Left padding for all cells
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),               # Right padding for all cells
        ])

        # Apply the style to the table
        table.setStyle(style)

        # Add the table to the elements list
        elements.append(table)



        # Add a spacer to increase the gap
        elements.append(Spacer(1, 36))

        # Create a table to place "Exam Cell In Charge" and "Head of the Department" on the same line
        in_charge_and_hod_table = Table([
            [Paragraph("Exam Cell In Charge:", getSampleStyleSheet()['BodyText']), Spacer(1, 1), Paragraph("Head of the Department:", getSampleStyleSheet()['BodyText'])]
        ], colWidths=[200, 100, 200])
        in_charge_and_hod_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]))
        elements.append(in_charge_and_hod_table)

    # Build PDF
    pdf.build(elements)

    # Get PDF content from buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    # Serve the PDF as a download
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=examallotment.pdf'
    return response




def download_room_report(request):
    # Query data from the Examallotment table
    examallotments = Examallotment.objects.all()

    # Create a PDF document
    pdf = SimpleDocTemplate("room_wise.pdf", pagesize=letter, leftMargin=36, rightMargin=36, topMargin=72, bottomMargin=72)
    elements = []

    # Variables to track the current room number
    current_room = None
    room_data = []

    for examallotment in examallotments:
        # If the current room changes, add the room data to elements and reset room_data
        if examallotment.RoomNo != current_room:
            if current_room is not None:
                elements.extend(get_room_elements(current_room, room_data))
                elements.append(PageBreak())  # Start a new page before the next room
            current_room = examallotment.RoomNo
            room_data = []

        # Append the current examallotment data to room_data
        room_data.append(examallotment)

    # Add the last room data to elements
    if current_room is not None:
        elements.extend(get_room_elements(current_room, room_data))

    # Build PDF
    pdf.build(elements)

    # Serve the PDF as a download
    with open("room_wise.pdf", "rb") as f:
        response = HttpResponse(f.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=room_wise.pdf'
        return response

def get_room_elements(room_number, room_data):
    # This function generates the elements for a room and returns them as a list
    elements = []

    # Add Aditya Engineering College logo on the left
    logo_path = 'C:/Users/devik/OneDrive/Pictures/Aditya.jpg'  # Update this with the path to your logo file
    logo = Image(logo_path, width=50, height=50)  # Adjust width and height to 25% of the original size

    # Add college name after the logo
    college_name = "Aditya Engineering College"
    college_name_para = Paragraph(college_name, getSampleStyleSheet()['Heading1'])

    # Create a table to arrange logo and college name side by side with reduced padding
    logo_college_table = Table([[logo, college_name_para]], colWidths=[100, 400])  # Adjust colWidths as needed

    # Set table properties with reduced padding
    logo_college_table.setStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertically
        ('LEFTPADDING', (0, 0), (-1, -1), 0),    # No left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),   # Reduced right padding
    ])

    # Add the table to the elements list
    elements.append(logo_college_table)

    # Add some space after the logo and college name
    elements.append(Spacer(1, 12))  # Reduced space after logo and college name

    # Add paragraphs for departments and venue
    elements.append(Paragraph("<b>Venue: </b>BGB", getSampleStyleSheet()['BodyText']))

    # Add room number
    elements.append(Paragraph("<b>Room Number: </b>{0}".format(room_number), getSampleStyleSheet()['BodyText']))

    students_per_bench = infer_students_per_bench(room_data)

    elements.append(Paragraph("<b>Students per Bench: </b>{0}".format(students_per_bench), getSampleStyleSheet()['BodyText']))
    elements.append(Spacer(1, 12))

    # Add grid of roll numbers
    roll_number_grid = create_roll_number_grid(room_data)
    elements.append(roll_number_grid)

    return elements

def infer_students_per_bench(room_data):
    # Count the number of students assigned to each bench
    bench_students_count = {}
    for examallotment in room_data:
        bench_number = examallotment.BenchNo
        if bench_number not in bench_students_count:
            bench_students_count[bench_number] = 0
        bench_students_count[bench_number] += 1
    
    # Determine the most common number of students per bench
    most_common_count = max(bench_students_count.values(), default=0)
    
    # Return the most common count as the inferred students per bench
    return most_common_count



def create_roll_number_grid(room_data):
    # Initialize a dictionary to store students per bench
    students_per_bench = {}

    # Count the number of students assigned to each bench
    for examallotment in room_data:
        bench_number = examallotment.BenchNo
        if bench_number not in students_per_bench:
            students_per_bench[bench_number] = []
        students_per_bench[bench_number].append(str(examallotment.Student_Id))

    # Determine the maximum number of students per bench
    max_students_per_bench = max(len(students) for students in students_per_bench.values())

    # Define the number of columns for the grid based on the maximum number of students per bench
    if max_students_per_bench == 3:
        num_columns = 9
    elif max_students_per_bench == 2:
        num_columns = 6
    else:
        num_columns = 3

    # Create a table for the roll number grid
    roll_number_data = []

    # Iterate over benches to fill rows with students
    current_row = []
    for bench_students in students_per_bench.values():
        if len(bench_students) < max_students_per_bench:
            bench_students.extend([''] * (max_students_per_bench - len(bench_students)))  # Fill empty slots if less than max students per bench
        current_row.extend(bench_students)
        if len(current_row) >= num_columns:
            # Add the current row to the roll_number_data
            roll_number_data.append(current_row[:num_columns])
            # Reset the current row for the next iteration
            current_row = current_row[num_columns:]

    # If there are remaining students, add them as a new row
    if current_row:
        # Fill empty slots at the end of the row
        current_row.extend([''] * (num_columns - len(current_row)))
        roll_number_data.append(current_row)

    # Define the column widths and space widths
    col_width = (215 * mm - 20 - (num_columns - 1) * 3) / num_columns  # Subtracting space widths from total width
    space_widths = [3 * mm] * (num_columns - 1)  # Space width after every 3 columns
    col_widths = [col_width] * num_columns + space_widths  # Add space widths to the column widths

    roll_number_table = Table(roll_number_data, colWidths=col_widths, hAlign='CENTER')
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Add left padding to the cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),  # Add right padding to the cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Increase bottom padding to increase cell height
        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Increase top padding to increase cell height
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add border (GRID) to cells
    ])
    roll_number_table.setStyle(style)

    return roll_number_table

