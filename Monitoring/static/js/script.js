const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');

uploadBtn.addEventListener('click', () => {
    fileInput.click(); 
});

fileInput.addEventListener('change', (event) => {
    const fileName = event.target.files[0] ? event.target.files[0].name : '';
    alert(`Выбран файл: ${fileName}`);
});

const filterInput = document.getElementById('filterInput');
const table = document.getElementById('myTable');
const rows = table.getElementsByTagName('tr');

filterInput.addEventListener('keyup', () => {
    const filter = filterInput.value.toLowerCase();
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let rowVisible = false;
        for (let j = 0; j < cells.length; j++) {
            if (cells[j].textContent.toLowerCase().includes(filter)) {
                rowVisible = true;
                break;
            }
        }
        rows[i].style.display = rowVisible ? '' : 'none';
    }
});

const filters = document.querySelectorAll('.filter');
const uniqueValues = Array.from({ length: 9 }, () => new Set());
for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName('td');
    uniqueValues[0].add(cells[0].textContent);
    uniqueValues[1].add(cells[1].textContent);
    uniqueValues[2].add(cells[2].textContent);
    uniqueValues[3].add(cells[3].textContent);
    uniqueValues[4].add(cells[4].textContent);
    uniqueValues[5].add(cells[5].textContent);
    uniqueValues[6].add(cells[6].textContent);
    uniqueValues[7].add(cells[7].textContent);
    uniqueValues[8].add(cells[8].textContent);
}

uniqueValues.forEach((set, index) => {
    const select = filters[index];
    set.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
});

function filterTable() {
    const filterValues = Array.from(filters).map(filter => filter.value);
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        const matches = filterValues.every((value, index) => 
            value === '' || cells[index].textContent === value
        );

        rows[i].style.display = matches ? '' : 'none';
    }
}

filters.forEach(filter => {
    filter.addEventListener('change', filterTable);
});

function register() {
    window.location.href = 'windowRegistration.html';
}

document.addEventListener("DOMContentLoaded", function() {
    let timeLeft = 60;
    const timerDisplay = document.getElementById("countdown-timer");
    const updateTimer = () => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        timeLeft--;
        if (timeLeft < 0) {
            clearInterval(timerInterval);
            timerDisplay.textContent = "Время вышло!";
        }
    };
    const timerInterval = setInterval(updateTimer, 1000);
    updateTimer();
});




