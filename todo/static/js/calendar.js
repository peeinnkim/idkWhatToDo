const init = {
  monList: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  dayList: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
  today: new Date(),
  monForChange: new Date().getMonth(),
  activeDate: new Date(),
  getFirstDay: (yy, mm) => new Date(yy, mm, 1),
  getLastDay: (yy, mm) => new Date(yy, mm + 1, 0),
  nextMonth: function () {
    let d = new Date();
    d.setDate(1);
    d.setMonth(++this.monForChange);
    this.activeDate = d;
    return d;
  },
  prevMonth: function () {
    let d = new Date();
    d.setDate(1);
    d.setMonth(--this.monForChange);
    this.activeDate = d;
    return d;
  },
  addZero: (num) => (num < 10) ? '0' + num : num,
  activeDTag: null,
  getIndex: function (node) {
    let index = 0;
    while (node = node.previousElementSibling) {
      index++;
    }
    return index;
  }
};

const $calBody = document.querySelector('.cal-body');
const $btnNext = document.querySelector('#cal-next');
const $btnPrev = document.querySelector('#cal-prev');
const $dateDisplay = document.querySelector('#show-fdate');

/*
  @param {date} fullDate
*/
function loadYYMM (fullDate) {
  let yy = fullDate.getFullYear();
  let mm = fullDate.getMonth();
  let firstDay = init.getFirstDay(yy, mm);
  let lastDay = init.getLastDay(yy, mm);
  let markToday;  // for marking today date

  if (mm === init.today.getMonth() && yy === init.today.getFullYear()) {
    markToday = init.today.getDate();
  }

  document.querySelector('#cur-month').textContent = init.monList[mm] + " " + yy;

  let trtd = '';
  let startCount;
  let countDay = 0;
  for (let i = 0; i < 6; i++) {
    trtd += '<tr>';
    for (let j = 0; j < 7; j++) {
      if (i === 0 && !startCount && j === firstDay.getDay()) {
        startCount = 1;
      }
      if (!startCount) {
        trtd += '<td>'
      } else {
        let fullDate = yy + '-' + init.addZero(mm + 1) + '-' + init.addZero(countDay + 1);
        trtd += '<td class="day';
        trtd += (markToday && markToday === countDay + 1) ? ' today"' : '"';
        trtd += ` data-date="${countDay + 1}" data-fdate="${fullDate}">`;
      }
      trtd += (startCount) ? ++countDay : '';
      if (countDay === lastDay.getDate()) {
        startCount = 0;
      }
      trtd += '</td>';
    }
    trtd += '</tr>';
  }
  $calBody.innerHTML = trtd;

}

loadYYMM(init.today);

$btnNext.addEventListener('click', () => loadYYMM(init.nextMonth()));
$btnPrev.addEventListener('click', () => loadYYMM(init.prevMonth()));

$calBody.addEventListener('click', (e) => {
  if (e.target.classList.contains('day')) {
    let day = Number(e.target.textContent);
    init.activeDTag = e.target;
    init.activeDate.setDate(day);
  }
});
