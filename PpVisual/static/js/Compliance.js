function GetGdpr_info(data) {
    var gdpr_data = data;
    var word_text =[];
    for(var i =0;i<gdpr_data.length;i++){
        var review = gdpr_data[i].review;
        var label_data = gdpr_data[i].label;
        word_text.push(review);
        if(label_data==0){
                var a0_text=review;
                weightsText(a0_text,"#1A2E49","white",label_data);
            }
            if(label_data==1){
                var a1_text=review;
                weightsText(a1_text,"#1A2E49","#1982c4",label_data);
            }
            if(label_data==2){
                var a2_text=review;
                weightsText(a2_text,"#1A2E49","#ffca3a",label_data);
            }
            if(label_data==3){
                var a3_text =review;
                weightsText(a3_text,"#1A2E49","#9c89b8",label_data);
            }

            if(label_data==4){
                var a4_text=review;
                weightsText(a4_text,"#1A2E49","#2ec4b6",label_data);

            }
            if(label_data==5){
                var a5_text=review;
                weightsText(a5_text,"#1A2E49","#ff595e",label_data)

            }
            if(label_data==6){
                var a6_text=review;
                weightsText(a6_text,"#1A2E49","#6a4c93",label_data)

            }
            if(label_data==7){
                var a7_text=review;
                weightsText(a7_text,"#1A2E49","#118ab2",label_data)

            }
            if(label_data==8){
                var a8_text=review;
                weightsText(a8_text,"#1A2E49","#83c5be",label_data);

            }
            if(label_data==9){
                var a9_text=review;
                weightsText(a9_text,"#1A2E49","#f0a6ca",label_data);

            }
            if(label_data==10){
                var a10_text=review;
                weightsText(a10_text,"#1A2E49","#9a8c98",label_data);
            }

    }
    WordClound(word_text);

}



    function weightsText(text, color1, color2,label_data) {
    var text_array=[];
    var text_data =text;
    var tooltips = d3.select("#OverviewText").append("div").attr("class", "tooltip").attr("opacity", 0.0);
    text_array.push(text_data);
    var colors = [ "white","#ffd2cc", "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93",
        "#118ab2", "#83c5be", "#f0a6ca","#9a8c98"];
    var svg1 =d3.select('#OverviewText').selectAll("text")
        .data(text_array)
        .enter()
        .append('span')
        .attr('id','text')
        .attr('id',"label_"+label_data)
        .attr('label',label_data)
        .attr('class','show_label')
        .style('color',function (d,i) {
            return colors[label_data];

        })
        .on("mouseover",function (d) {
            var label_type = d3.select(this).attr("label");
            var app_label = ["其他","收集个人数据","数据存储期限",  "收集数据目的", "联系方式", "访问数据权", "擦除或更改权", "限制处理权", "拒绝处理权", "数据携带权", "申诉权"];
            // const label_too = label;
            tooltips.html( "标签类型:"+app_label[label_type])
                // .attr("x", (d3.event.pageX + 30) + "px")
                // .attr("y", (d3.event.pageY + 200) + "px")
                .style("opacity", 1.0)
                .style("color","white");

        })
        .on("mouseout",function (d) {
            tooltips.style("opacity", 0.0);
        })
        .text(function (text_array){
            return text_array;})
        .append('br');


    }
// function bar(label_data) {
//     var app_label = ["未提到数据存储期限",  "未提到收集数据目的", "未提到联系方式", "未提到访问数据权", "未提到擦除或更改权", "未提到限制处理权", "未提到拒绝处理权", "未提到数据携带权", "未提到申诉权"];
//     var sale = [41, 47, 33, 94, 20, 75, 46, 36, 14];
//     var bar_width = 320;
//     var bar_height = 360;
//     var svg = d3.select("div#corlor_bar").append("svg").attr("width", bar_width).attr("height", bar_height);
//
//     const padding = {
//         top: 10,
//         right: 20,
//         bottom: 205,
//         left: 60,
//     }
//
//
//     var xScale = d3.scale.ordinal().domain(app_label).rangeRoundBands([0, bar_width - padding.left - padding.right]);
//     var xAxis = d3.svg.axis()
//         .scale(xScale)
//         .orient("bottom");
//     var yScale = d3.scale.linear()
//         .domain([0, d3.max(sale)])
//         .range([bar_height - padding.top - padding.bottom, 0]);
//     var yAxis = d3.svg.axis()
//         .scale(yScale)
//         .orient("left");
//     var rectPadding = 4;
//     var max = d3.max(sale);
//     var colors = new Array( "#1982c4", "#ffca3a", "#9c89b8", "#2ec4b6", "#ff595e", "#6a4c93", "#118ab2",
//         "#83c5be", "#f0a6ca", "#9a8c98");
//     var rects = svg.selectAll(".MyRect")
//         .data(sale)
//         .enter()
//         .append("rect")
//         .attr("class", "MyRect")
//         .attr("transform", "translate(" + padding.left + "," + padding.top + ")")
//         .attr("x", function(d, i) {
//             return i * (xScale.rangeBand()) + rectPadding / 4;
//         })
//         .attr("y", function(d) {
//             return yScale(d);
//         })
//         .attr("width", xScale.rangeBand())
//         .attr("height", function(d) {
//             return bar_height - padding.top - padding.bottom - yScale(d);
//         })
//         .attr("fill", function(d, i) {
//             return colors[i];
//         });
//     var texts = svg.selectAll(".MyText")
//         .data(sale)
//         .enter()
//         .append("text")
//         .attr("class", "MyText")
//         .attr("transform", "translate(" + padding.left + "," + padding.top + ")")
//         .attr("x", function(d, i) {
//             return i * (xScale.rangeBand()) + rectPadding / 2;
//         })
//         .attr("y", function(d) {
//             return yScale(d);
//         })
//         .attr("dx", function() {
//             return (xScale.rangeBand() - rectPadding) / 2;
//         })
//         .attr("dy", function(d) {
//             return 10;
//         })
//         .text(function(d) {
//             return d;
//         })
//         .style({
//             "fill": "#FFF",
//             "dominant-baseline": "middle",
//             'font-size': 10,
//             "font-family":"courier"
//         });
//
//     svg.append("g")
//         .attr("class", "axis axis--x")
//         .attr("transform", "translate(" + padding.left + "," + (bar_height - padding.bottom) + ")")
//         .call(xAxis)
//         .attr("fill","white")
//         .selectAll("text")
//         .style("text-anchor", "end")
//         .attr("dx", "-.8em")
//         .attr("dy", ".10em")
//         .attr("id",function (d,i) {
//             return "label_bar"+label_data[i];
//         })
//         .attr("transform", "rotate(-65)")
//         .style({
//             'font-size': 15,
//             "font-family":"courier"
//         });
//
//     //添加y轴
//     svg.append("g")
//         .attr("class", "axis axis--y")
//         .attr("transform", "translate(" + padding.left + "," + padding.top + ")")
//         .call(yAxis)
//         .attr("fill","white")
//         .style({
//
//             'font-size': 15,
//             "font-family":"courier"
//         });
//
// }


    // d3.csv("./data/compliance.csv", function (data) {
    //     // console.log(data);
    //     var com_could=[];
    //     for(var i=0;i<data.length;i++){
    //         var words = data[i].word;
    //         var weight = data[i].weight;
    //         if(weight>0.65){
    //             var keyword =words;
    //             // console.log(keyword);
    //             var com_word={}
    //             com_word.word = keyword;
    //             com_word.size = weight;
    //
    //             com_could.push(com_word);
    //         }
    //     }
    //     // console.log(keywords);
    //     // console.log(com_could);
    //     // WordClound(com_could)
    // });
    function WordClound(com_could) {
        var myWords = com_could.toString();
        console.log(myWords.toString());
        var common = "poop,i,me,my,myself,we,us,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,whose,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,will,would,should,can,could,ought,i'm,you're,he's,she's,it's,we're,they're,i've,you've,we've,they've,i'd,you'd,he'd,she'd,we'd,they'd,i'll,you'll,he'll,she'll,we'll,they'll,isn't,aren't,wasn't,weren't,hasn't,haven't,hadn't,doesn't,don't,didn't,won't,wouldn't,shan't,shouldn't,can't,cannot,couldn't,mustn't,let's,that's,who's,what's,here's,there's,when's,where's,why's,how's,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,upon,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,say,says,said,shall";

        var word_count = {};

        var words = myWords.split(/[ '\-\(\)\*":;\[\]|{},.!?]+/);
        if (words.length == 1){
            word_count[words[0]] = 1;
        } else {
            words.forEach(function(word){
                var word = word.toLowerCase();
                if (word != "" && common.indexOf(word)==-1 && word.length>1){
                    if (word_count[word]){
                        word_count[word]++;
                    } else {
                        word_count[word] = 1;
                    }
                }
            })
        }

        var svg_location = "div#tsne";
        var width = 400;
        var height = 300;

        var fill = d3.scale.category10();

        var word_entries = d3.entries(word_count);

        var xScale = d3.scale.linear()
            .domain([0, d3.max(word_entries, function(d) {
                return d.value;
            })
            ])
            .range([10,100]);

        d3.layout.cloud().size([width, height])
            .timeInterval(20)
            .words(word_entries)
            .fontSize(function(d) { return xScale(+d.value); })
            .text(function(d) { return d.key; })
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .on("end", draw)
            .start();

        function draw(words) {
            d3.select(svg_location).append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return xScale(d.value) + "px"; })
                .style("font-family", "Impact")
                .style("fill", function(d, i) { return fill(i); })
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.key; });
        }

        d3.layout.cloud().stop();

        

    }


