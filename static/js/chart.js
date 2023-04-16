const TotalShowBlocks = 16; //默认展示的块数40，始终表示不变
const LevelTexts = ["0", "差", "25", "中", "50", "良", "75", "优", "100"]; //用于展示的刻度
const ShowPercent = 0.75; //用于展示的仪表盘角度的百分比，剩下的是透明的
const TotalBlocks = Math.floor(16 / ShowPercent);
const StartAngle = -180 + 90 - (360 * (1 - ShowPercent)) / 2;
const KeduLength = 2; //每5个显示一个刻度
const Value = 60; //表示目标数值
const Kedu = 100 / TotalShowBlocks;

function rgbToHex(r, g, b) {
  var hex = ((r << 16) | (g << 8) | b).toString(16);
  return "#" + new Array(Math.abs(hex.length - 7)).join("0") + hex;
}

// hex to rgb
function hexToRgb(hex) {
  var rgb = [];
  for (var i = 1; i < 7; i += 2) {
    rgb.push(parseInt("0x" + hex.slice(i, i + 2)));
  }
  return rgb;
}

// 计算渐变过渡色 startColor:初始色号，endColor最终色号，step渐变步数
function gradient(startColor, endColor, step) {
  // 将 hex 转换为rgb
  var sColor = hexToRgb(startColor),
    eColor = hexToRgb(endColor);

  // 计算R\G\B每一步的差值
  var rStep = (eColor[0] - sColor[0]) / step,
    gStep = (eColor[1] - sColor[1]) / step,
    bStep = (eColor[2] - sColor[2]) / step;

  var gradientColorArr = [];
  for (var i = 0; i < step; i++) {
    // 计算每一步的hex值
    gradientColorArr.push(
      rgbToHex(
        parseInt(rStep * i + sColor[0]),
        parseInt(gStep * i + sColor[1]),
        parseInt(bStep * i + sColor[2])
      )
    );
  }
  return gradientColorArr;
}

let grades = [];
let grades_txt = [];
const objValue = Math.ceil(Value / Kedu); //55表示目标数值，2.5是仪表盘上每个单位代表的数值
const colorArr = gradient("#8e0c00", "#f42800", TotalBlocks);

for (let i = 0; i < TotalBlocks; i++) {
  //取40作为需要设置的块数
  let item = {
    name: i === objValue ? "55.5%" : "",
    value: 1,
  };
  if (i === objValue) {
    //目标位置，需要被选中的
    // item.selected = true  选中后默认有位移
    item.label = {
			selected: false,
      borderColor: colorArr[objValue],
      borderWidth: 0,
      width: 9,
      height: 9,
      borderRadius: 20,
      color: "transparent",
      backgroundColor: "#fff",
    };
  }
  grades.push(item);
  grades_txt.push({
    name: "",
    value: 1,
  });
}

option = {
  grid: {
    top: 40,
  },
  series: [
    //用于画一个圆形的线，修饰用
    {
      name: "",
      type: "pie",
      radius: ["64%", "65%"],
			selectedMode: false,
			selectedOffset: 0,
      data: [
        //长度为1一位数组，画单色线
        {
          value: 1,
          name: Value+"%",
          label: {
            color: "#ccc",
            fontSize: 10,
          },
        },
      ],
      itemStyle: {
        color: "#dedede", //线的颜色
      },
      label: {
        position: "center", //内容展示在圆形正中间
      },
    },
    {
      name: "", //刻度文字
      type: "pie",
			selectedMode: false,
			selectedOffset: 0,
      radius: ["65%", "82%"],
      data: grades_txt.concat([1 / 1000]), //越小越好，更接近起点
      startAngle: StartAngle,
      label: {
        position: "inside",
        formatter: (props = { value }) => {
          const { value, dataIndex } = props;
          // console.log(props,dataIndex)
          // const labels = ["0", "优", "25", "良", "50", "中", "75", "差", "100"];
          // //5
          // if (
          //   (dataIndex + 1) % KeduLength === 0 &&
          //   dataIndex < TotalShowBlocks
          // ) {
          //   return labels[(dataIndex + 1) / KeduLength];
          // } else if (dataIndex === TotalBlocks) {
          //   return "0";
          // }
          return null;
        },
        color: "#AEAEAE",
        fontSize: 10,
      },
      itemStyle: {
        color: "transparent",
      },
    },
    {
      name: "",
      type: "pie",
      radius: ["85%", "100%"],
      startAngle: StartAngle,
			selectedMode: false,
			selectedOffset: 0,
      itemStyle: {
        shadowColor: "rgba(255, 255, 255, 1)",
        shadowBlur: 2,
        borderWidth: 1,
        color: (props) => {
          const { seriesIndex, dataIndex, data, value } = props;
          if (dataIndex >= TotalShowBlocks) {
            return "transparent";
          } else {
            return colorArr[dataIndex];
          }
        },
      },
      label: {
        position: "inner",
        backgroundColor: "transparent",
        rich: {
          a: {
            color: "transparent",
            lineHeight: 32,
            align: "center",
          },
        },
      },
      data: grades,
    },
  ],
};

let myEchart = echarts.init(document.getElementById("usage"));
myEchart.setOption(option);
window.addEventListener("resize", () => {
  myEchart.resize();
});
