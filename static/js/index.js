let thingList = document.querySelector(".thingList");

const lightRed = document.querySelector(".lightRed");
const lightGreen = document.querySelector(".lightGreen");
const button = document.querySelector(".button");
let PerName = document.querySelector(".name");

var person = {
  name : PerName.textContent,
};
let timeDiv = document.querySelector(".time");
setInterval(() => {
  timeDiv.innerHTML = new Date().format("yyyy-MM-dd hh:mm:ss");
}, 1000);

const normalRed = "#00ff00";
const normalGreen = "#f42800";
const darkRed = "#193e10";
const darkGreen = "#491408";

let labels = [
  "打火机",
  "压力容器",
  "刀",
  "充电宝",
  "打火机油",
  "手铐",
  "弹弓",
  "鞭炮",
  "尖锐工具",
  "甩棍",
  "电棍",
];

labels.forEach((label) => {
  thingList.insertAdjacentHTML(
    "beforeend",
    `<div class="thingItemNormal">
			<div class="detailWrapper">
				<div>${label}</div>													
		</div>
		</div>`
  );
});

Date.prototype.format = function (fmt) {
  let o = {
    "M+": this.getMonth() + 1, //月份
    "d+": this.getDate(), //日
    "h+": this.getHours(), //小时
    "m+": this.getMinutes(), //分
    "s+": this.getSeconds(), //秒
    "q+": Math.floor((this.getMonth() + 3) / 3), //季度
    S: this.getMilliseconds(), //毫秒
  };
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(
      RegExp.$1,
      (this.getFullYear() + "").substr(4 - RegExp.$1.length)
    );
  }
  for (let k in o) {
    if (new RegExp("(" + k + ")").test(fmt)) {
      fmt = fmt.replace(
        RegExp.$1,
        RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length)
      );
    }
  }
  return fmt;
};

let state = false;
let interval = setInterval(() => {
  fetch("/state")
    .then((e) => e.json())
    .then((e) => {
      //console.log(e);
      try {
        let index = labels.findIndex((label) => label === e.label);
        if (thingList.children[index].className == "thingItemDanger") {
          clearTimeout(thingList.children[index].timer);
          thingList.children[index].timer = setTimeout(() => {
            thingList.children[index].className = "thingItemNormal";
          }, 2000);
        } else {
          thingList.children[index].className = "thingItemDanger";
          thingList.children[index].timer = setTimeout(() => {
            thingList.children[index].className = "thingItemNormal";
          }, 2000);
        }
} catch (e) {
}	if(!state) {
		if (e.state) {
		state = true;
		setTimeout(()=>{state=false}, 1000)
		  lightGreen.style.backgroundColor = normalGreen;
		  lightRed.style.backgroundColor = darkRed;
		} else {
		
		  lightGreen.style.backgroundColor = darkGreen;
		  lightRed.style.backgroundColor = normalRed;
		}
	}

    });
}, 300);

button.onclick = function(){
  if (PerName.textContent != '无')
    window.open('/' + PerName.textContent, '_blank')
}

setInterval(() => {
  fetch("/name").then((e) => e.json())
  .then((e) =>{
    PerName.textContent = e.name;
  })
}, 500);

function renderChart() {
  fetch('/data')
    .then(response => response.json())
    .then(data => {
      const chartData = data.data;
      const chartLabels = chartData.map(d => d.hour);
      const chartValues = chartData.map(d => d.count);

      const ctx = document.getElementById('chart').getContext('2d');
      const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
            datasets: [{
                label: '违禁品数量',
                backgroundColor: 'rgba(255, 99, 132, 0.8)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                data: [12, 19, 3, 5, 2, 3, 10, 6, 9, 12, 20, 22, 16, 14, 18, 24, 22, 19, 15, 12, 10, 8, 6, 4],
            }]
        },
        options: {
            animation: {
                duration: 2000,
                easing: 'easeInOutQuad'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                labels: {
                    fontColor: '#fff'
                }
            },
            title: {
                display: true,
                text: '违禁品检测数量统计',
                fontColor: '#fff',
                fontSize: 36
            }
        }
    });
    });
}
// 在页面加载时渲染图表
window.onload = function() {
  renderChart();
};