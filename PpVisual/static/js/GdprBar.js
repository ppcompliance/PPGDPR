function GetBar(data) {
    console.log("data",data)
    var json_data = JSON.stringify(data)

    var appParse = JSON.parse(json_data);
    var label_a = appParse.toString().split(",");
    var gdprlabel_data=label_a.map(Number);
    var sum = arrSum(gdprlabel_data);
    var gdprlabel_data = gdprlabel_data.map(function (num) {
        return (num/sum).toFixed(2);
    });
    console.log(gdprlabel_data);
    var app_label = ["未提到数据存储期限",  "未提到收集数据目的", "未提到联系方式", "未提到访问数据权", "未提到擦除或更改权", "未提到限制处理权", "未提到拒绝处理权", "未提到数据携带权", "未提到申诉权"];
    var label_data=[0,1,2,3,4,5,6,7,8,9];
    var bar_width = 320;
    var bar_height = 360;
    var svg = d3.select("div#corlor_bar").append("svg").attr("width", bar_width).attr("height", bar_height);
    var padding = {
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
        .domain([0, d3.max(gdprlabel_data)])
        .range([bar_height - padding.top - padding.bottom, 0]);
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left");
    var rectPadding = 4;
    var max = d3.max(gdprlabel_data);
    var colors = new Array( "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93", "#118ab2",
        "#83c5be", "#f0a6ca", "#9a8c98");
    var rects = svg.selectAll(".MyRect")
        .data(gdprlabel_data)
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
        .data(gdprlabel_data)
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
        .attr("fill","white")
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".10em")
        .attr("id",function (d,i) {
            return "label_bar"+label_data[i];
        })
        .attr("transform", "rotate(-65)")
        .style({
            'font-size': 15,
            "font-family":"courier"
        });

    //添加y轴
    svg.append("g")
        .attr("class", "axis axis--y")
        .attr("transform", "translate(" + padding.left + "," + padding.top + ")")
        .call(yAxis)
        .attr("fill","white")
        .style({

            'font-size': 15,
            "font-family":"courier"
        });


}
function arrSum(data){
	console.log("arry",data);
	 var s = 0;
	 data.forEach(function(val, idx, data) {
	        s += val;
	    }, 0);
	    return s;

}