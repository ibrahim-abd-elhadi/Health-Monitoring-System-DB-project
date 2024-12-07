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

    // 3. Enable dragging for patient cards container
    const patientCardsContainer = document.getElementById('patient-cards-container');
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

    // 4. Search functionality
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    const patientCards = document.querySelectorAll('.patient-card');

    searchButton.addEventListener('click', function () {
        const searchTerm = searchInput.value.toLowerCase();
        patientCards.forEach(card => {
            const patientName = card.querySelector('.patient-info strong').innerText.toLowerCase();
            if (patientName.includes(searchTerm)) {
                card.style.display = 'flex'; // Show matching cards
            } else {
                card.style.display = 'none'; // Hide non-matching cards
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById('searchInput');
    const patientCardsContainer = document.querySelector('.patient-cards'); // التأكد من أن هذه هي العنصر الصحيح
    const patientCards = document.querySelectorAll('.patient-card');

    searchButton.addEventListener('click', function () {
        const searchTerm = searchInput.value.trim().toLowerCase();

        // إذا كان حقل الإدخال فارغًا، لا نفعل شيء
        if (searchTerm === "") {
            return;
        }

        let found = false;

        patientCards.forEach(card => {
            const patientName = card.querySelector('.patient-info strong').innerText.toLowerCase();

            if (patientName.includes(searchTerm)) {
                found = true;

                // إظهار البطاقة المطابقة فقط أولاً
                card.parentElement.prepend(card);

                // إخفاء جميع البطاقات الأخرى
                patientCards.forEach(c => {
                    if (c !== card) {
                        c.style.display = 'none';
                    }
                });
            }
        });

        // إذا لم يتم العثور على تطابق، إخفاء جميع البطاقات
        if (!found) {
            patientCards.forEach(card => card.style.display = 'none');
        }
    });

    // عند مسح النص في حقل الإدخال، إرجاع جميع البطاقات
    searchInput.addEventListener('input', function () {
        if (searchInput.value.trim() === "") {
            patientCards.forEach(card => {
                card.style.display = 'flex'; // إظهار جميع البطاقات عند مسح النص
            });
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const patientList = document.querySelector('.patient-cards');

    
    // إضافة مستمع للأزرار الحالية عند تحميل الصفحة
    document.querySelectorAll('.patient-card .close-btn').forEach(button => {
        button.addEventListener('click', async function () {
            let patient_id = document.querySelector('.patient-info').attributes['data-patient-id'].value;

            await fetch('http://127.0.0.1:5000/patient_profile', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    'patient_id': patient_id
                })
            })

            const card = this.closest('.patient-card');
            patientList.removeChild(card);
        });
    });

    // إضافة مريض جديد مع زر حذف يعمل عند الضغط على زر Add
    const addButton = document.querySelector('.add-patient-button');
    const defaultImageSrc = "/static/images/download.jpg";

    addButton.addEventListener('click', () => {
        // تحقق من العدد الحالي للبطاقات
        const currentPatientCount = document.querySelectorAll('.patient-card').length;
        if (currentPatientCount >= 5) return; // لا تضيف المزيد إذا كانت هناك 5 بطاقات

        const newCard = document.createElement('li');
        newCard.classList.add('patient-card');

        const patientImage = document.createElement('img');
        patientImage.src = defaultImageSrc;
        patientImage.alt = 'New Patient';

        const patientInfo = document.createElement('div');
        patientInfo.classList.add('patient-info');

        const patientName = document.createElement('strong');
        patientName.textContent = document.getElementById('username').value || 'New Patient';

        const status = document.createElement('p');
        status.textContent = 'Status: Good';

        const reason = document.createElement('p');
        reason.textContent = 'Reason: Checkup';

        const appointment = document.createElement('p');
        appointment.textContent = 'Appointment: 6:00 PM';

        // زر الحذف
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('close-btn');
        deleteButton.innerHTML = '&#10006;';
        deleteButton.addEventListener('click', function () {
            patientList.removeChild(newCard);
        });

        patientInfo.appendChild(patientName);
        patientInfo.appendChild(status);
        patientInfo.appendChild(reason);
        patientInfo.appendChild(appointment);

        newCard.appendChild(patientImage);
        newCard.appendChild(patientInfo);
        newCard.appendChild(deleteButton);

        patientList.appendChild(newCard);
        document.getElementById('username').value = ''; // تفريغ حقل الاسم
    });
});
