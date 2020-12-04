var textarray1 =[];var textarray2=[];var textarray3=[];var textarray4=[];var textarray5=[];var textarray6=[];
var textarray7 =[];var textarray8=[];var textarray9=[];var textarray10=[];var textarray11=[];
function getMain(data) {
        console.log("data",data);

        for(var i=0; i<data.length;i++) {
            var text = data[i].review;
            var label_data = data[i].label;

            if (label_data == 0) {
                textarray1.push(text);
                var a0_text = text;
                weightsText(text, "#1A2E49", "#ffd2cc", label_data);
                // annotate_keywords(a0_text);
            }
            if (label_data == 1) {
                textarray2.push(text);
                // console.log(text);
                var a1_text = text;
                weightsText(a1_text, "#1A2E49", "#1982c4", label_data)
            }
            if (label_data == 2) {
                textarray3.push(text);
                var a2_text = text;
                weightsText(a2_text, "#1A2E49", "#ffca3a", label_data);
            }
            if (label_data == 3) {
                textarray4.push(text);
                var a3_text = text;
                weightsText(a3_text, "#1A2E49", "#9c89b8", label_data);
            }

            if (label_data == 4) {
                textarray5.push(text);
                var a4_text = text;
                weightsText(a4_text, "#1A2E49", "#2ec4b6", label_data);

            }
            if (label_data == 5) {
                textarray6.push(text);
                var a5_text = text;
                weightsText(a5_text, "#1A2E49", "#ff595e", label_data)

            }
            if (label_data == 6) {
                textarray7.push(text);
                var a6_text = text;
                weightsText(a6_text, "#1A2E49", "#6a4c93", label_data)

            }
            if (label_data == 7) {
                textarray8.push(text);
                var a7_text = text;
                weightsText(a7_text, "#1A2E49", "#118ab2", label_data)

            }
            if (label_data == 8) {
                textarray9.push(text);
                var a8_text = text;
                weightsText(a8_text, "#1A2E49", "#83c5be", label_data);

            }
            if (label_data == 9) {
                textarray10.push(text);
                var a9_text = text;
                weightsText(a9_text, "#1A2E49", "#f0a6ca", label_data);

            }
            if (label_data == 10) {
                textarray11.push(text);
                var a10_text = text;
                weightsText(a10_text, "#1A2E49", "#9a8c98", label_data);
            }
        }
        Button();
        console.log("11111",textarray1);
        //饼图

     var obj = {}, k, arr1 = [];
        for (var i = 0, len = data.length; i < len; i++) {
            k = data[i].label;
            if (obj[k])
                obj[k]++;
            else
                obj[k] = 1;
        }
        //保存结果{0-'元素'，count-出现次数}
        for (var o in obj) {
            arr1.push([o, obj[o]]);
        }
        var pie = d3.layout.pie().sort(null).value(function (d) {
            return d[1];
        });
        var piedata = pie(arr1);
        var width = 300;
        var height = 300;
        var radius = Math.min(width,height) / 2;
        var svg = d3.select("div#corlor_bar").append("svg").attr("width", width).attr("height", height).attr("text-align", "center").attr("class","label_Pie");
        // var outerRadius = width / 3;           // 外半径
        // var innerRadius = 0;             // 内半径
        // var arc = d3.svg.arc().innerRadius(innerRadius).outerRadius(outerRadius);
        var arc = d3.svg.arc().innerRadius(radius * 0.8).outerRadius(radius * 0.4);
        var color = new Array("#ffd2cc", "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93", "#118ab2", "#83c5be", "#f0a6ca", "#9a8c98");
        var arcs = svg.selectAll("g").data(piedata).enter().append("g").attr("transform", "translate(" + (width / 2.5) + "," + (height / 2.5) + ")");
        arcs.append("path").attr("fill", function (d, i) {

            return color[d.data[0]];
        }).attr("d", function (d) {
            return arc(d);
        });
        arcs.append("text").attr("transform", function (d) {
            var x = arc.centroid(d)[0] * 1.0;
            var y = arc.centroid(d)[1] * 1.0;
            return "translate(" + x + "," + y + ")";
            // return "translate(" + arc.centroid(d)[0] + ")";
        }).attr('text-anchor', 'middle').text(function (d) {
            return d.data[1];
        });
        var tooltip = d3.select("div#corlor_bar").append("div").attr("class", "tooltip").attr("opacity", 0.0);

        arcs.on("mouseover", function (d, i) {
             var label_dict=["隐私介绍",  "第一方收集信息和使用", "Cookies以及相似技术", "第三方收集和分享数据", "用户选项及权力", "数据安全", "数据保留", "国际数据存储及转移", "特殊人群","隐私政策修改","隐私政策联系信息"];

            console.log(label_dict[i] + "标签的数量为" + "<br />" + d.data[1])
            tooltip.html(label_dict[i] + "标签的数量为" + "<br />" + d.data[1])
                .style("left", (d3.event.pageX-40) + "px")
                .style("top", (d3.event.pageY -150) + "px")
                .style("opacity", 1.0)
                .style("color","white");

        })
            .on("mousemover", function (d) {
                tooltip.style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY -100) + "px");
            })
            .on("mouseout", function (d) {

                tooltip.style("opacity", 0.0);
            })




}
//文本主体
function weightsText (text,color1,color2,label) {
    var text_array=[];
    var text_main =text;
    text_array.push(text_main);
    var svg =d3.select('#OverviewText').selectAll("text")
            .data(text_array)
            .enter()
            .append('span')
            .attr('id','text')
            .attr('id',"label_"+label)
            .attr('label',label)
            .attr('class','show_label')
            .text(function (text_array){
            return text_array;})
            .append('br');
}
function Button(){
        $(".button").click(function(){
            var buttonId = $(this).attr('id');
            if(buttonId == "one") {Introduction();}
            if(buttonId == "two") {FristUseCollection();}
            if(buttonId == "three") {Cookies();}
            if(buttonId == "four"){ThirdParty()}
            if(buttonId == "five"){UserRight()}
            if(buttonId =="six"){DataSecurity()}
            if(buttonId == "seven"){DataRetention()}
            if(buttonId == "eight"){InternationalData()}
            if(buttonId == "nine"){SpecialPop()}
            if(buttonId == "ten"){PPChange()}
            if(buttonId =="eleven"){PPContact()}
            $('#modal-container').removeAttr('class').addClass('one');
            $('.data_content').attr("id","content");
            // $('body').addClass('modal-active');
        })

        $('#modal-container').click(function(){
            $(this).addClass('out');
            // $('body').removeClass('modal-active');
            $('.data_content').removeAttr("id");
            $("#TextShow").empty();
            $("#chart").empty();
            $("#River").empty();
        });
    }
function Introduction() {
        var texts =textarray1;
        console.log(texts);
        $("#River").empty();
        TimeRive("static/data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("span")
            .data(TextOne)
            .enter()
            .append("span")
            .attr("class", 'textshow')
            .text(d => d.textword);
        // annotate_keywords(texts);
    }
    function FristUseCollection() {
        var texts =textarray2;

        d3.csv("data/test.csv", function(error, data){
            var textONe=[];
            if(error){
                console.log(error);
            }
            // console.log(data);
            for (var i = 0; i < data.length; i++){
                FristUse_label = data[i].label;
                FristUse_sentence = data[i].sentence;
                if(FristUse_label=="collect your name"){
                    textONe.push(FristUse_sentence);
                    var collect_text=FristUse_sentence;
                }
            }
            var FristUse_text=[];
            var text_Frist = textONe;
            for (var i =0; i<text_Frist.length; i++){
                FristUse_text.push({textword:text_Frist[i]})
            }
            // console.log(FristUse_text);
            // $("#TextShow").empty();
            // $("#chart").empty();
            d3.select("#TextShow")
                .selectAll("p")
                .data(FristUse_text)
                .enter()
                .append("p")
                .attr("class", 'textshow')
                .style("color","#ff595e")
                .text(d => d.textword);
        });
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);

        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#chart")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function Cookies() {
        var texts =textarray3;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function ThirdParty() {
        var texts =textarray4;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function UserRight() {
        var texts =textarray5;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function DataSecurity() {
        var texts =textarray6;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function DataRetention() {
        var texts =textarray7;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function InternationalData() {
        var texts =textarray8;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function SpecialPop() {
        var texts =textarray9;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function PPChange() {
        var texts =textarray10;
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }
    function PPContact() {
        var texts =textarray11;
        console.log(texts);
        console.log("2",texts);
        $("#River").empty();
        TimeRive("data/data.csv","orange");
        var TextOne = [];
        for (var i =0; i < texts.length; i++)
        {
            TextOne.push({textword:texts[i]})
        }
        // console.log(TextOne);
        $("#TextShow").empty();
        $("#chart").empty();
        d3.select("#TextShow")
            .selectAll("p")
            .data(TextOne)
            .enter()
            .append("p")
            .attr("class", 'textshow')
            .text(d => d.textword);

    }

    var datearray = [];
    var colorrange = [];
    function TimeRive(data,color) {
            if (color == "blue") {
                colorrange = ["#045A8D", "#2B8CBE", "#74A9CF", "#A6BDDB", "#D0D1E6", "#F1EEF6"];
            }
            else if (color == "pink") {
                colorrange = ["#980043", "#DD1C77", "#DF65B0", "#C994C7", "#D4B9DA", "#F1EEF6"];
            }
            else if (color == "orange") {
                colorrange = ["#ffd2cc"];
            }
            strokecolor = colorrange[0];

            var format = d3.time.format("%m/%d/%y");

            var margin = {top: 20, right: 40, bottom: 30, left: 40};
            var width = 400 - margin.left - margin.right;
            var height = 200 - margin.top - margin.bottom;

            var tooltip = d3.select("body")
                .append("div")
                .attr("class", "remove")
                .style("position", "absolute")
                .style("z-index", "20")
                .style("visibility", "hidden")
                .style("top", "30px")
                .style("left", "55px");

            var x = d3.time.scale()
                .range([0, width]);

            var y = d3.scale.linear()
                .range([height-10, 0]);

            var z = d3.scale.ordinal()
                .range(colorrange);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom")
                .ticks(d3.time.weeks);

            var yAxis = d3.svg.axis()
                .scale(y);

            var yAxisr = d3.svg.axis()
                .scale(y);

            var stack = d3.layout.stack()
                .offset("silhouette")
                .values(function(d) { return d.values; })
                .x(function(d) { return d.date; })
                .y(function(d) { return d.value; });

            var nest = d3.nest()
                .key(function(d) { return d.key; });

            var area = d3.svg.area()
                .interpolate("cardinal")
                .x(function(d) { return x(d.date); })
                .y0(function(d) { return y(d.y0); })
                .y1(function(d) { return y(d.y0 + d.y); });

            var svg = d3.select(".timeRiver").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var graph = d3.csv(data, function(data) {
                data.forEach(function(d) {
                    d.date = format.parse(d.date);
                    d.value = +d.value;
                });

                var layers = stack(nest.entries(data));

                x.domain(d3.extent(data, function(d) { return d.date; }));
                y.domain([0, d3.max(data, function(d) { return d.y0 + d.y; })]);

                svg.selectAll(".layer")
                    .data(layers)
                    .enter().append("path")
                    .attr("class", "layer")
                    .attr("d", function(d) { return area(d.values); })
                    .style("fill", function(d, i) { return z(i); });


                svg.append("g")
                    .attr("class", "x axis")
                    .attr("transform", "translate(0," + height + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("class", "y axis")
                    .attr("transform", "translate(" + width + ", 0)")
                    .call(yAxis.orient("right"));

                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis.orient("left"));

                svg.selectAll(".layer")
                    .attr("opacity", 1)
                    .on("mouseover", function(d, i) {
                        svg.selectAll(".layer").transition()
                            .duration(250)
                            .attr("opacity", function(d, j) {
                                return j != i ? 0.6 : 1;
                            })})

                    .on("mousemove", function(d, i) {
                        mousex = d3.mouse(this);
                        mousex = mousex[0];
                        var invertedx = x.invert(mousex);
                        invertedx = invertedx.getMonth() + invertedx.getDate();
                        var selected = (d.values);
                        for (var k = 0; k < selected.length; k++) {
                            datearray[k] = selected[k].date
                            datearray[k] = datearray[k].getMonth() + datearray[k].getDate();
                        }

                        mousedate = datearray.indexOf(invertedx);
                        pro = d.values[mousedate].value;

                        d3.select(this)
                            .classed("hover", true)
                            .attr("stroke", strokecolor)
                            .attr("stroke-width", "0.5px"),
                            tooltip.html( "<p>" + d.key + "<br>" + pro + "</p>" ).style("visibility", "visible");

                    })
                    .on("mouseout", function(d, i) {
                        svg.selectAll(".layer")
                            .transition()
                            .duration(250)
                            .attr("opacity", "1");
                        d3.select(this)
                            .classed("hover", false)
                            .attr("stroke-width", "0px"), tooltip.html( "<p>" + d.key + "<br>" + pro + "</p>" ).style("visibility", "hidden");
                    })

                var vertical = d3.select(".timeRiver")
                    .append("div")
                    .attr("class", "remove")
                    .style("position", "absolute")
                    .style("z-index", "19")
                    .style("width", "1px")
                    .style("height", "380px")
                    .style("top", "10px")
                    .style("bottom", "30px")
                    .style("left", "0px")
                    .style("background", "#fff");

                d3.select(".chart")
                    .on("mousemove", function(){
                        mousex = d3.mouse(this);
                        mousex = mousex[0] + 5;
                        vertical.style("left", mousex + "px" )})
                    .on("mouseover", function(){
                        mousex = d3.mouse(this);
                        mousex = mousex[0] + 5;
                        vertical.style("left", mousex + "px")});
            });
        }