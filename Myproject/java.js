document.addEventListener('DOMContentLoaded', () => {
    // 1. Toggle submenu visibility
    const submenuTriggers = document.querySelectorAll('.sidebar-menu li span');
    submenuTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const submenu = trigger.nextElementSibling;
            if (submenu && submenu.tagName === 'UL') {
                submenu.classList.toggle('visible');
            }
        });
    });

    // 2. Highlight the active menu item
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
    });

    // بيانات المرضى
    const patientData = [
        { name: "Mark", status: "Good", reason: "Diabetes", appointment: "6:00 PM" },
        { name: "Bill", status: "Good", reason: "Hypertension", appointment: "7:00 PM" },
        { name: "Steve", status: "Good", reason: "Flu", appointment: "8:00 PM" }
    ];

    const patientCardsContainer = document.querySelector('.patient-cards');
    const usernameInput = document.getElementById('username');
    const addButton = document.querySelector('.add-patient-button');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');

    // قائمة المرضى المضافة
    const addedPatients = new Set();

    // إزالة البطاقات الموجودة عند تحميل الصفحة
    patientCardsContainer.innerHTML = '';

    // إضافة مريض جديد
    addButton.addEventListener('click', () => {
        const username = usernameInput.value.trim().toLowerCase();

        if (!username) {
            alert("Please enter a valid username.");
            return;
        }

        // منع الإضافة إذا كان حقل البحث غير فارغ
        if (searchInput.value.trim()) {
            alert("Clear the search field before adding a patient.");
            return;
        }

        const patient = patientData.find(p => p.name.toLowerCase() === username);

        if (!patient) {
            alert("Patient not found in database.");
            return;
        }

        // التحقق إذا كانت البطاقة مضافة بالفعل
        if (addedPatients.has(username)) {
            alert("This patient is already added.");
            return;
        }

        // إنشاء البطاقة
        const patientCard = document.createElement('li');
        patientCard.classList.add('patient-card');
        patientCard.innerHTML = `
            <div class="patient-info">
                <strong>${patient.name}</strong>
                <p>Status: ${patient.status}</p>
                <p>Reason: ${patient.reason}</p>
                <p>Appointment: ${patient.appointment}</p>
            </div>
            <button class="close-btn">×</button>
        `;
        patientCardsContainer.appendChild(patientCard);

        // إضافة المريض إلى قائمة المرضى المضافة
        addedPatients.add(username);

        // تفريغ الحقل
        usernameInput.value = '';
    });

    // البحث عن مريض
    searchButton.addEventListener('click', () => {
        const query = searchInput.value.trim().toLowerCase();

        Array.from(patientCardsContainer.children).forEach(card => {
            const name = card.querySelector('.patient-info strong').textContent.toLowerCase();
            card.style.display = name.includes(query) ? '' : 'none';
        });
    });

    // عرض البطاقات عند مسح النص في البحث
    searchInput.addEventListener('input', () => {
        if (!searchInput.value.trim()) {
            Array.from(patientCardsContainer.children).forEach(card => {
                card.style.display = '';
            });
        }
    });

    // حذف بطاقة مريض
    patientCardsContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('close-btn')) {
            const card = event.target.closest('.patient-card');
            const name = card.querySelector('.patient-info strong').textContent.toLowerCase();

            // إزالة البطاقة من قائمة المرضى المضافة
            addedPatients.delete(name);

            // إزالة البطاقة من الواجهة
            patientCardsContainer.removeChild(card);
        }
    });

    // إضافة خاصية السحب (dragging) للبطاقات
    let isDragging = false;
    let startY = 0;
    let scrollStart = 0;

    patientCardsContainer.addEventListener('mousedown', (e) => {
        isDragging = true;
        startY = e.pageY;
        scrollStart = patientCardsContainer.scrollTop;
        patientCardsContainer.style.cursor = 'grabbing';
    });

    patientCardsContainer.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const deltaY = e.pageY - startY;
        patientCardsContainer.scrollTop = scrollStart - deltaY;
    });

    patientCardsContainer.addEventListener('mouseup', () => {
        isDragging = false;
        patientCardsContainer.style.cursor = 'grab';
    });

    patientCardsContainer.addEventListener('mouseleave', () => {
        if (isDragging) {
            isDragging = false;
            patientCardsContainer.style.cursor = 'grab';
        }
    });
});
