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
				<div>物品名称</div>
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