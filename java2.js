document.addEventListener('DOMContentLoaded', () => {
    const submenuTriggers = document.querySelectorAll('.sidebar-menu li span');
    submenuTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const submenu = trigger.nextElementSibling;
            if (submenu && submenu.tagName === 'UL') {
                submenu.classList.toggle('visible');
            }
        });
    });

    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
    });

    // Initialize calendar date
    let currentDate = new Date();
    let month = currentDate.getMonth(); // 0 is January, 1 is February, etc.
    let year = currentDate.getFullYear();
    const appointments = {}; // Object to store appointment info by date

    // Get elements
    const monthYear = document.getElementById("monthYear");
    const calendarGrid = document.getElementById("calendarGrid");
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');  // Corrected input id
    const addAppointmentButton = document.querySelector('.patient-info button');

    // Function to generate the calendar grid for a given month and year
    function generateCalendar(month, year) {
        // Set the month and year text
        monthYear.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${year}`;

        // Clear the grid before adding new days
        calendarGrid.innerHTML = '';
        // Add days of the week row
        const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        daysOfWeek.forEach(day => {
            const dayElement = document.createElement('div');
            dayElement.classList.add('calendar-day');
            dayElement.textContent = day;
            calendarGrid.appendChild(dayElement);
        });

        // Get the first day of the month (0 is Sunday, 1 is Monday, etc.)
        const firstDay = new Date(year, month, 1).getDay();
        // Get the number of days in the month
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Create empty divs for the days before the 1st
        for (let i = 0; i < firstDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.classList.add('calendar-day', 'empty');
            calendarGrid.appendChild(emptyDay);
        }

        // Create the days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.classList.add('calendar-day');
            dayElement.textContent = day;

            // Check if this day has an appointment
            const dateKey = `${year}-${month + 1}-${day}`;
            if (appointments[dateKey]) {
                dayElement.style.backgroundColor = 'red';
                dayElement.style.color = 'white';
                dayElement.textContent = appointments[dateKey].time; // Replace the day number with the time
            }

            // Click event to select a day and input time
            dayElement.addEventListener('click', () => {
                dateInput.value = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                // Check if the selected day already has an appointment
                if (appointments[dateKey]) {
                    alert(`This day already has an appointment scheduled at ${appointments[dateKey].time}`);
                }
            });

            calendarGrid.appendChild(dayElement);
        }
    }

    // Event listeners for navigation buttons
    document.getElementById("prevMonth").addEventListener("click", () => {
        month--;
        if (month < 0) {
            month = 11;
            year--;
        }
        currentDate.setMonth(month); // Update currentDate with the new month
        generateCalendar(month, year);
    });

    document.getElementById("nextMonth").addEventListener("click", () => {
        month++;
        if (month > 11) {
            month = 0;
            year++;
        }
        currentDate.setMonth(month); // Update currentDate with the new month
        generateCalendar(month, year);
    });

    // Event listener for the Add Appointment button
    addAppointmentButton.addEventListener('click', () => {
        const selectedDate = new Date(dateInput.value);
        const today = new Date();

        // Ensure the selected date is valid and greater than today by at least one day
        if (!isNaN(selectedDate) && selectedDate > today) {
            const dateKey = `${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}`;
            const time = timeInput.value; // Get time from the patient-info input field
            if (time) {
                // Check if there's already an appointment on this day
                if (appointments[dateKey]) {
                    alert(`This day already has an appointment scheduled at ${appointments[dateKey].time}`);
                } else {
                    appointments[dateKey] = { time }; // Store the appointment time
                    generateCalendar(month, year); // Regenerate calendar to reflect the change
                }
            } else {
                alert('Please enter a valid time for the appointment.');
            }
        } else {
            alert('Please select a valid date that is at least one day in the future.');
        }
    });

    // Generate the initial calendar
    generateCalendar(month, year);
});
