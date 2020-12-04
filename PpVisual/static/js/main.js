(function () {
    var textarray1 =[];var textarray2=[];var textarray3=[];var textarray4=[];var textarray5=[];var textarray6=[];
    var textarray7 =[];var textarray8=[];var textarray9=[];var textarray10=[];var textarray11=[];
    d3.json("./static/data/data110.json", function(error, data) {
        if (error) {
            console.log(error);
        }
        // policyMinmap(data);

        for (var i = 0; i < data.length; i++) {
            var text = data[i].review;
            const label_data = data[i].label;
            const weig = data[i].word_weight;
            const arrParse = JSON.parse(weig);
            const w = arrParse.toString().split(",");
            const weight = w.map(Number);
            if(label_data==0){
                textarray1.push(text);
                var a0_text=text;
                weightsText(a0_text,weight,"#1A2E49","#ffd2cc",label_data);
                // annotate_keywords(a0_text);
            }
            if(label_data==1){
                textarray2.push(text);
                // console.log(text);
                var a1_text=text;
                weightsText(a1_text,weight,"#1A2E49","#1982c4",label_data)
            }
            if(label_data==2){
                textarray3.push(text);
                var a2_text=text;
                weightsText(a2_text,weight,"#1A2E49","#ffca3a",label_data);
            }
            if(label_data==3){
                textarray4.push(text);
                var a3_text =text;
                weightsText(a3_text,weight,"#1A2E49","#9c89b8",label_data);
            }

            if(label_data==4){
                textarray5.push(text);
                var a4_text=text;
                weightsText(a4_text,weight,"#1A2E49","#2ec4b6",label_data);

            }
            if(label_data==5){
                textarray6.push(text);
                var a5_text=text;
                weightsText(a5_text,weight,"#1A2E49","#ff595e",label_data)

            }
            if(label_data==6){
                textarray7.push(text);
                var a6_text=text;
                weightsText(a6_text,weight,"#1A2E49","#6a4c93",label_data)

            }
            if(label_data==7){
                textarray8.push(text);
                var a7_text=text;
                weightsText(a7_text,weight,"#1A2E49","#118ab2",label_data)

            }
            if(label_data==8){
                textarray9.push(text);
                var a8_text=text;
                weightsText(a8_text,weight,"#1A2E49","#83c5be",label_data);

            }
            if(label_data==9){
                textarray10.push(text);
                var a9_text=text;
                weightsText(a9_text,weight,"#1A2E49","#f0a6ca",label_data);

            }
            if(label_data==10){
                textarray11.push(text);
                var a10_text=text;
                weightsText(a10_text,weight,"#1A2E49","#9a8c98",label_data);
            }
        }
        Button();

        // if(textarray1!=null){
        //     Button(textarray1);
        // }
        // if(textarray2!=null){
        //     Button(textarray1);
        // }
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
            const label_dict=["隐私介绍",  "第一方收集信息和使用", "Cookies以及相似技术", "第三方收集和分享数据", "用户选项及权力", "数据安全", "数据保留", "国际数据存储及转移", "特殊人群","隐私政策修改","隐私政策联系信息"];

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


    });


    var margin = {top: 10, right: 20, bottom: 180, left: 80},
        width = 400 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    var x0 = d3.scale.ordinal()
        .rangeRoundBands([0, width], 0.5);

    var x1 = d3.scale.ordinal();

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x0)
        .tickSize(0)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");


    var color = new Array("#ffd2cc", "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93", "#118ab2", "#83c5be", "#f0a6ca", "#9a8c98");
    var svg = d3.select('div#bar').append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    d3.json("data/data.json", function(error, data) {

        var categoriesNames = data.map(function(d) { return d.categorie; });
        var rateNames = data[0].values.map(function(d) { return d.rate; });
        // console.log(rateNames);

        x0.domain(categoriesNames);
        x1.domain(rateNames).rangeRoundBands([0, x0.rangeBand()]);
        y.domain([0, d3.max(data, function(categorie) { return d3.max(categorie.values, function(d) { return d.value; }); })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-40)")
            .attr("fill","white");

        svg.append("g")
            .attr("class", "y axis")
            .attr("fill","white")
            .style('opacity','0')
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .style('font-weight','bold');

        svg.select('.y').transition().duration(100).delay(1600).style('opacity','1');
        var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d,i) {
                console.log(d.data);
                return "<strong style='color: white'>"+(d.rate)+"</strong> <span style='color:red'>" + d.value + "</span>";
            });
        svg.call(tip);
        var slice = svg.selectAll(".slice")
            .data(data)
            .enter().append("g")
            .attr("class", "g")
            .attr("transform",function(d) { return "translate(" + x0(d.categorie) + ",0)"; });



        slice.selectAll("rect")
            .data(function(d) { return d.values; })
            .enter().append("rect")
            .attr("class","rect")
            .attr("width", x1.rangeBand())
            .attr("x", function(d) { return x1(d.rate); })
            // .attr("x", function(d) { return x1(d.rate); })
            .style("fill", function (d, i) {
                var colo=color[d.label];
                return colo;
            })
            .attr("y", function(d) { return y(0); })
            .attr("height", function(d) { return height - y(0); })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        slice.selectAll("rect")
            .transition()
            .delay(function (d) {return Math.random()*1000;})
            .duration(1000)
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); });

        // Legend
        // var legend = svg.selectAll(".legend")
        //     .data(data[0].values.map(function(d) { return d.rate; }).reverse())
        // .enter().append("g")
        //     .attr("class", "legend")
        //     .attr("transform", function(d,i) { return "translate(0," + i * 20 + ")"; })
        //     .style("opacity","0");

        // legend.append("rect")
        //     .attr("x", width - 18)
        //     .attr("width", 1118)
        //     .attr("height", 18)
        //     .style("fill", function(d,i) { return color[i]; });

        // legend.append("text")
        //     .attr("x", width - 24)
        //     .attr("y", 9)
        //     .attr("dy", ".35em")
        //     .style("text-anchor", "end")
        //     .text(function(d) {return d; });

        // legend.transition().duration(500).delay(function(d,i){ return 1300 + 100 * i; }).style("opacity","1");

    });





    // function annotate_keywords(text) {
    //     d3.csv("./data/keyword.csv", function (data) {
    //         // console.log(data);
    //         var keywords = [];
    //         var data_weight = [];
    //         for (var i = 0; i < data.length; i++) {
    //             var words = data[i].word;
    //             var weight = data[i].weight;
    //             keywords.push(words);
    //             data_weight.push(weight);
    //         }
    //         var tmp = text.toString();
    //         var bb = keywords;
    //         for(var i = 0;i < bb.length;i++){
    //             var KeyWord = bb[i];
    //             var reg = new RegExp("(\\b" + KeyWord + "\\b)");
    //             tmp = tmp.replace(reg,"<b class='keyword' style='background-color: red' >$1</b>")
    //             console.log(tmp);
    //             $(this).html(tmp + "<br>");
    //         }
    //     });
    //
    //
    // }





    function weightsText (text,word_weight,color1,color2,label) {
        var text_array=[];
        var text_data =text;
        // var tooltips = d3.select("#OverviewText").append("div").attr("class", "tooltip").attr("opacity", 0.0);
        text_array.push(text_data);
        // var color = d3.scale.linear().domain().range(color2);
        // console.log(color2);
        // console.log(text_array);
        // var width = 720;
        // var h =  20;
        // const translate = 15;
        var svg =d3.select('#OverviewText').selectAll("text")
            .data(text_array)
            .enter()
            .append('span')
            .attr('id','text')
            .attr('id',"label_"+label)
            .attr('label',label)
            .attr('class','show_label')
            // .on("mouseover",function (d) {
            //     var label_type = d3.select(this).attr("label");
            //     // console.log(label_type);
            //     var app_label = ["隐私介绍",  "第一方收集信息和使用", "Cookies以及相似技术", "第三方收集和分享数据", "用户选项及权力", "数据安全", "数据保留", "国际数据存储及转移", "特殊人群","隐私政策修改","隐私政策联系信息"];
            //     // const label_too = label;
            //     tooltips.html( "标签类型:"+app_label[label_type])
            //         // .attr("x", (d3.event.pageX + 30) + "px")
            //         // .attr("y", (d3.event.pageY + 200) + "px")
            //         .style("opacity", 1.0)
            //         .style("color","white");
            //
            // })
            // .on("mouseout",function (d) {
            //     tooltips.style("opacity", 0.0);
            // })
            .text(function (text_array){
            return text_array;})
            .append('br');


        var label_too = label;
        // KeyWord(text_data,"Computer");
        // const weights =word_weight;
        // var text = text;
        // const width = 720;
        // const letterwidth = {};
        // const w = width;
        // const div = document.createElement('div');
        // div.style.float = 'left';
        // document.body.appendChild(div);
        // let i = text.length;
        // while (i--) {
        //     let letter = text.charAt(i-1);
        //     div.innerText = letter;
        //     let computerWidth = window.getComputedStyle(div, null).getPropertyValue("width").match(/\d+/)[0];
        //     letterwidth[letter] = parseInt(computerWidth);
        // }
        // let maxLength = 0;
        // text.split(" ").forEach(d => {
        //     let length = 0;
        //     var i = d.length;
        //     while (i--) {
        //         length += letterwidth[d.charAt(i)];
        //     }
        //     if (length > maxLength) {
        //         maxLength = length;
        //     }
        // });
        // let xText = 0;
        // let yText = 0;
        // const color = d3.scale.linear().domain([0, d3.max(weights)]).range([color1, color2]);
        // const words = text.split(" ").map((d, index) => {
        //     let length = 0;
        //     var i = d.length;
        //     while (i--) {
        //         length += letterwidth[d.charAt(i)];
        //     }
        //     let newWidthText = xText + 15 + length;
        //     if (newWidthText > w - 50) {
        //         xText = 0;
        //         yText += 20;
        //         newWidthText = 10 + length;
        //     }
        //     let value = {
        //         xText: xText,
        //         yText: yText,
        //         word: d,
        //         weight: weights[index],
        //         width: length + 20,
        //     };
        //     xText = newWidthText;
        //     return value;
        // });
        // const translate = 15;
        // const h = translate + (yText + 8);
        // const svg = d3.select('div.center_text').append("svg").attr("width", width+10).attr("height", h).attr("class","label"+label);
        //
        // // console.log(words);
        // svg.append("g").attr("transform", `translate(50, ${translate})`).selectAll("rect").data(words).enter().append("rect").attr("x", d => d.xText - 27).attr("y", d => d.yText - 15).attr("width", d => d.width).attr("height", 18).attr("fill", d => color(d.weight));
        // svg
        //     .append("g")
        //     .attr("transform", `translate(50, ${translate})`)
        //     .attr("class","labeltext"+label)
        //     .selectAll("text")
        //     .data(words)
        //     .enter()
        //     .append("text")
        //     .attr("fill","white")
        //     .attr("class", "word")
        //     .attr("index",d => d.word)
        //     .attr("x", d => d.xText-25)
        //     .attr("y", d => d.yText)
        //     .text(d => d.word);

        // var tooltips = d3.select("div.policyMinimap").append("div").attr("class", "tooltips").attr("opacity", 0.0);
        // label_too = label;
        // var ste =svg.on("mouseover",function(label_too,words,i,d){
        //     console.log(label_too);
        //
        //     var app_label = ["隐私介绍",  "第一方收集信息和使用", "Cookies以及相似技术", "第三方收集和分享数据", "用户选项及权力", "数据安全", "数据保留", "国际数据存储及转移", "特殊人群","隐私政策修改","隐私政策联系信息"];
        //
        //     var x =d3.event.pageX;
        //     var y =d3.event.pageY+30;
        //
        //     tooltips.transition()
        //         .duration(200)+。
        //     console.log("标签为"  + app_label[label])
        //     tooltips.html( "标签类型:"+app_label[label])
        //         .style("left", x)
        //         .style("top", y)
        //         .style("opacity", 1.0);
        //     tooltips.style("box-shadow", "10px 0px 0px" + color(i));
        // })
        //     .on("mouseout", function (label_too,words,i,d) {
        //         var tool = tooltips.style("opacity", 0);
        //         return tool;
        //     })

        // var obj = {}, k, arr1 = [];
        // for (var i = 0, len = data.length; i < len; i++) {
        //     k = data[i].label;
        //     if (obj[k])
        //         obj[k]++;
        //     else
        //         obj[k] = 1;
        // }
        // //保存结果{0-'元素'，count-出现次数}
        // for (var o in obj) {
        //     arr1.push([o, obj[o]]);
    }
    //匹配关键字
    // function KeyWord(str, key) {
    //     var textHight = str
    //     var reg = new RegExp("d3.select("#OverviewText")(" + key + ")", "g");
    //     var newstr = textHight.replace(reg, "<span style='background:red;'>$1</span>");
    //     return newstr;
    // }





    function policyMinmap(data) {
        const sentNum=[];
        for (var i = 0; i < data.length; i++) {
            const text = data[i].review;
            const textLen = text.split(" ");
            const sum_sent=textLen.length;
            sentNum.push(sum_sent);
        }

        let text_long = eval(sentNum.join("+"));
        // console.log(text_long);
        // let textLen=0;
        // let sun_redult=[];
        // try {
        //     textLen = text_orig.split(" ");
        // }catch (e) {
        //
        // }
        // sum_sent=textLen.length;
        // console.log(sun_redult,"->label:",label);
        // // console.log(typeof (textLen));
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
        // console.log(texts);
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

    //匹配每个标签下的关键词
    // function annotate_keywords(text) {
    //     d3.csv("./data/keyword.csv", function (data) {
    //         // console.log(data);
    //         var keywords =[];
    //         var data_weight=[];
    //         for(var i=0;i<data.length;i++){
    //             var words = data[i].word;
    //             var weight = data[i].weight;
    //             keywords.push(words);
    //             data_weight.push(weight);
    //         }
    //
    //     });
    //     console.log(text.toString());
    //     // console.log(keywords)
    //
    // }







    //时间序列变化图
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




    //属性提取图




})();