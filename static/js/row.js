class myScroll {
    constructor(param) {
      this.target = document.getElementById(param.id)
      this.space = param.space || 102
      this.target.classList.add('KatyLightScrollRowsBox')
      this.content = this.target.querySelector('.content')
      this.scrollBox = document.createElement('div')
      this.scrollBox.classList.add('scrollBox')
      this.target.append(this.scrollBox)
      this.leftBtn = document.createElement('div')
      this.leftBtn.classList.add('left')
      this.scrollBox.append(this.leftBtn)
      this.scroll = document.createElement('div')
      this.scroll.classList.add('scroll')
      this.scrollBox.append(this.scroll)
      this.rightBtn = document.createElement('div')
      this.rightBtn.classList.add('right')
      this.scrollBox.append(this.rightBtn)
      this.bar = document.createElement('div')
      this.bar.classList.add('bar')
      this.scroll.append(this.bar)

      this.maxWidth = this.content.firstElementChild.clientWidth
      this.viewWidth = this.content.clientWidth
      this.scrollWidth = this.scroll.clientWidth
      this.barWidth = Math.floor(this.viewWidth / this.maxWidth * this.viewWidth)
      this.slideWidth = this.scrollWidth - this.barWidth
      this.bar.style.width = this.barWidth + 'px'
      this.endLeft = this.scrollWidth - this.barWidth
      this.mouseLeft = 0
      this.moveWidth = this.maxWidth - this.viewWidth

      this.beginMoveZ = this.beginMove.bind(this)
      this.moveZ = this.move.bind(this)
      this.moveToZ = this.moveTo.bind(this)
      this.endMoveZ = this.endMove.bind(this)
      this.leftZ = this.left.bind(this)
      this.rightZ = this.right.bind(this)
      this.bar.addEventListener('mousedown', this.beginMoveZ)
      this.scroll.addEventListener('click', this.moveToZ)
      this.leftBtn.addEventListener('click', this.leftZ)
      this.rightBtn.addEventListener('click', this.rightZ)
      this.leftNum = 0
    }

    update(){
      this.maxWidth = this.content.firstElementChild.clientWidth
      this.viewWidth = this.content.clientWidth
      this.scrollWidth = this.scroll.clientWidth
      this.barWidth = Math.floor(this.viewWidth / this.maxWidth * this.viewWidth)
      this.slideWidth = this.scrollWidth - this.barWidth
      this.bar.style.width = this.barWidth + 'px'
      this.endLeft = this.scrollWidth - this.barWidth
      this.mouseLeft = 0
      this.moveWidth = this.maxWidth - this.viewWidth
      let left=this.leftNum
      this.content.scrollLeft = left / this.endLeft * (this.maxWidth - this.viewWidth)

      this.bar.style.left = left + 'px'
    }
    beginMove(e) {
      document.addEventListener('mousemove', this.moveZ)
      document.addEventListener('mouseup', this.endMoveZ)
      let rect = this.bar.getBoundingClientRect()
      this.mouseLeft = e.x - rect.left
    }

    move(e) {
      let rect = this.scroll.getBoundingClientRect()
      let left = e.x - rect.left
      if (left < 0) {
        left = 0
      } else if (rect.right - e.x < 0) {
        left = this.endLeft
      } else {
        left = left - this.mouseLeft
        if (left < 0) {
          left = 0
        } else if (left > this.endLeft) {
          left = this.endLeft
        }
      }
      this.leftNum = left
      this.content.scrollLeft = left / this.endLeft * (this.maxWidth - this.viewWidth)

      this.bar.style.left = left + 'px'

    }

    moveTo(e) {
      if (e.target !== this.bar) {
        let left = Math.floor(e.offsetX - this.barWidth / 2)
        if (left < 0) {
          left = 0
        } else if (left > this.endLeft) {
          left = this.endLeft
        }
        this.leftNum = left
        this.content.scrollLeft = left / this.endLeft * this.moveWidth
        this.bar.style.left = left + 'px'

      }
    }

    right(e) {
      let left = this.leftNum + this.space/this.moveWidth*this.endLeft
      if (left < 0) {
        left = 0
      } else if (left > this.endLeft) {
        left = this.endLeft
      }
      this.content.scrollLeft = left / this.endLeft * this.moveWidth
      this.bar.style.left = left + 'px'
      this.leftNum = left

    }

    left(e) {
      let left = this.leftNum - this.space/this.moveWidth*this.endLeft
      if (left < 0) {
        left = 0
      } else if (left > this.endLeft) {
        left = this.endLeft
      }
      this.content.scrollLeft = left / this.endLeft * this.moveWidth
      this.bar.style.left = left + 'px'
      this.leftNum = left
    }

    endMove(e) {
      document.removeEventListener('mousemove', this.moveZ)
      document.removeEventListener('mouseup', this.endMoveZ)
    }
  }

let prohibited_item = document.querySelector(".item img");
let Passenger_name = document.querySelector('.name').textContent;

var my
window.onload = () => {
my = new myScroll({ id: 'ab' ,space:100})
setTimeout(()=>{
    my.update();
},1500)
}

setInterval(() => {
  if (Passenger_name != 'undefined')
  {
    fetch("/items/"+Passenger_name).then((e) => e.json())
    .then((e) =>{
      prohibited_item.src = 'data:image/png;base64,' + e.items_data;
    })
  }
}, 500);