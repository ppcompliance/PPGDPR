(function(){
	var numset = [];
	d3.csv("./data/GDPR_label.csv", function(error, csvdata) {
		if (error) {
			console.log(error);
		}
		console.log(csvdata);
		for (var i = 0; i < csvdata.length; i++) {
			var review = csvdata[i].review;
			var label_data = csvdata[i].label;
			 if(label_data==0){
							var a0_text=review;
			                weightsText(a0_text,"#ffffff","#ffd2cc",label_data);
						}
						if(label_data==1){
							var a1_text=review;
							weightsText(a1_text,"#ffffff","#1982c4",label_data)
						}
						if(label_data==2){
							var a2_text=review;
							weightsText(a2_text,"#ffffff","#ffca3a",label_data);
						}
						if(label_data==3){
			                var a3_text =review;
			                weightsText(a3_text,"#ffffff","#9c89b8",label_data);
						}
			
						if(label_data==4){
			                var a4_text=review;
			                weightsText(a4_text,"#ffffff","#2ec4b6",label_data);
			
						}
						if(label_data==5){
			                var a5_text=review;
			                weightsText(a5_text,"#ffffff","#ff595e",label_data)
			
						}
						if(label_data==6){
			                var a6_text=review;
			                weightsText(a6_text,"#ffffff","#6a4c93",label_data)
			
						}
						if(label_data==7){
			                var a7_text=review;
			                weightsText(a7_text,"#ffffff","#118ab2",label_data)
			
						}
						if(label_data==8){
			                var a8_text=review;
			                weightsText(a8_text,"#ffffff","#83c5be",label_data);
			
						}
						if(label_data==9){
			                var a9_text=review;
			                weightsText(a9_text,"#ffffff","#f0a6ca",label_data);
			
						}
						if(label_data==10){
			                var a10_text=review;
			                weightsText(a10_text,"#ffffff","#9a8c98",label_data);
						}
		}
	});
	
	
	function weightsText(text, color1, color2,label_data) {
		label =label_data;
		weights = text.split(" ").map(d => Math.random())
		// console.log(weights);
		const width = 600;
		const letterwidth = {};
		const w = width;
		const div = document.createElement('div');
		div.style.float = 'left';
		document.body.appendChild(div);
		let i = text.length;
		while (i--) {
			let letter = text.charAt(i-1)
			div.innerText = letter;
			let computerWidth = window.getComputedStyle(div, null).getPropertyValue("width").match(/\d+/)[0];
			letterwidth[letter] = parseInt(computerWidth);
		}
		let maxLength = 0
		text.split(" ").forEach(d => {
			let length = 0;
			var i = d.length;
			while (i--) {
				length += letterwidth[d.charAt(i)];
			}
			if (length > maxLength) {
				maxLength = length;
			}
		})
		let xText = 0;
		let yText = 0;
		const color = d3.scale.linear().domain([0, d3.max(weights)]).range([color1, color2]);
		const words = text.split(" ").map((d, index) => {
			let length = 0;
			var i = d.length;
			while (i--) {
				length += letterwidth[d.charAt(i)];
			}
			let newWidthText = xText + 10 + length;
			if (newWidthText > w - 50) {
				xText = 0;
				yText += 20;
				newWidthText = 10 + length;
			}
			let value = {
				xText: xText,
				yText: yText,
				word: d,
				weight: weights[index],
				width: length + 20,
			};
			xText = newWidthText;
			return value;
		});
		const translate = 15;
		const h = translate + (yText + 20);
		const svg = d3.select('div.chart').append("svg").attr("width", width).attr("height", h).attr("class","label_"+label);
	
		svg.append("g").attr("transform", `translate(50, ${translate})`).selectAll("rect").data(words).enter().append("rect")
			.attr("x", d => d.xText - 2).attr("y", d => d.yText - 15).attr("width", d => d.width).attr("height", 18).attr(
				"fill", d => color(d.weight));
		svg
			.append("g")
			.attr("transform", `translate(50, ${translate})`)
			.selectAll("text")
			.data(words)
			.enter()
			.append("text")
			.attr("class", d =>d.label)
			.attr("x", d => d.xText)
			.attr("y", d => d.yText)
			.text(d => d.word);
	
	
	}
	
	var app_label = ["未提到数据存储期限",  "未提到收集数据目的", "未提到联系方式", "未提到访问数据权", "未提到擦除或更改权", "未提到限制处理权", "未提到拒绝处理权", "未提到数据携带权", "未提到申诉权"];
	var sale = [41, 47, 33, 94, 20, 75, 46, 36, 14];
	var bar_width = 320;
	var bar_height = 360;
	var svg = d3.select("div#corlor_bar").append("svg").attr("width", bar_width).attr("height", bar_height);
	
	const padding = {
		top: 10,
		right: 20,
		bottom: 205,
		left: 60,
	}
	
	
	var xScale = d3.scale.ordinal().domain(app_label).rangeRoundBands([0, bar_width - padding.left - padding.right]);
	var xAxis = d3.svg.axis()
		.scale(xScale)
		.orient("bottom");
	var yScale = d3.scale.linear()
		.domain([0, d3.max(sale)])
		.range([bar_height - padding.top - padding.bottom, 0]);
	var yAxis = d3.svg.axis()
		.scale(yScale)
		.orient("left");
	var rectPadding = 4;
	var max = d3.max(sale);
	var colors = new Array( "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93", "#118ab2",
		"#83c5be", "#f0a6ca", "#9a8c98");
	var rects = svg.selectAll(".MyRect")
		.data(sale)
		.enter()
		.append("rect")
		.attr("class", "MyRect")
		.attr("transform", "translate(" + padding.left + "," + padding.top + ")")
		.attr("x", function(d, i) {
			return i * (xScale.rangeBand()) + rectPadding / 4;
		})
		.attr("y", function(d) {
			return yScale(d);
		})
		.attr("width", xScale.rangeBand())
		.attr("height", function(d) {
			return bar_height - padding.top - padding.bottom - yScale(d);
		})
		.attr("fill", function(d, i) {
			return colors[i];
		});
	var texts = svg.selectAll(".MyText")
		.data(sale)
		.enter()
		.append("text")
		.attr("class", "MyText")
		.attr("transform", "translate(" + padding.left + "," + padding.top + ")")
		.attr("x", function(d, i) {
			return i * (xScale.rangeBand()) + rectPadding / 2;
		})
		.attr("y", function(d) {
			return yScale(d);
		})
		.attr("dx", function() {
			return (xScale.rangeBand() - rectPadding) / 2;
		})
		.attr("dy", function(d) {
			return 10;
		})
		.text(function(d) {
			return d;
		})
		.style({
			"fill": "#FFF",
			"dominant-baseline": "middle",
			'font-size': 10,
			"font-family":"courier"
		});
	svg.append("g")
		.attr("class", "axis axis--x")
		.attr("transform", "translate(" + padding.left + "," + (bar_height - padding.bottom) + ")")
		.call(xAxis)
		.selectAll("text")
		.style("text-anchor", "end")
		.attr("dx", "-.8em")
		.attr("dy", ".10em")
		.attr("transform", "rotate(-65)")
		.style({
			"fill": "balck",
			'font-size': 15,
			"font-family":"courier"
		});
	
	//添加y轴
	svg.append("g")
		.attr("class", "axis axis--y")
		.attr("transform", "translate(" + padding.left + "," + padding.top + ")")
		.call(yAxis)
		.style({
			"fill": "balck",
			'font-size': 15,
			"font-family":"courier"
		});
	
})();
