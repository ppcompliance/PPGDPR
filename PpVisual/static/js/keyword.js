function getKeyWord(keyword) {
    var data = keyword;
     var keywords =[];
        var data_weight=[];
        for(var i=0;i<data.length;i++){
            var words = data[i].word;
            var weight = data[i].weight;
            keywords.push(words);
            data_weight.push(weight);
        }
        annotate_keywords(keywords,data_weight)
}
 function annotate_keywords(keywords,data_weight) {
        $(".center_text").each(function () {
            $(this).find('span').each(function () {
                var tmp = $(this).text();
                // console.log(tmp);
                var bb = keywords;
                // console.log(bb);
                var label = d3.select(this).attr("label");
                for (var i = 0; i < bb.length; i++) {
                    var KeyWord =bb[i];
                    var reg = new RegExp("(\\b" + KeyWord + "\\b)");
                    // console.log(reg);
                    tmp = tmp.replace(reg, "<b class='keyword'>$1</b>");
                    $(this).html(tmp + "<br>");
                }
            })
            // document.getElementById("text").innerHTML=result;

        })
        var data_weight=data_weight;
        // console.log(data_weight);
        var color1='#0A6379',color2='#059EB8';
        var tooltips = d3.select("#OverviewText").append("div").attr("class", "tooltip").attr("opacity", 0.0);
        var color = d3.scale.linear().domain([0,d3.max(data_weight)]).range([color1,color2]);
        var svg = d3.selectAll('.keyword').data(keywords).attr("weight", function (d,i) {
            return data_weight[i];
        });

        var svg1 = d3.selectAll('.keyword').style("background",function(d){
            return color(d3.select(this).attr("weight"));
        })
            .on("mouseover",function (d) {
                var label_type = $(this).parent().attr("label");
                var app_label = ["隐私介绍",  "第一方收集信息和使用", "Cookies以及相似技术", "第三方收集和分享数据", "用户选项及权力", "数据安全", "数据保留", "国际数据存储及转移", "特殊人群","隐私政策修改","隐私政策联系信息"];
                // const label_too = label;
               var x = d3.mouse(this)[0];
               var y = d3.mouse(this)[1];
                tooltips.html( "标签类型:"+app_label[label_type])
                    .style("opacity", 1.0)
                    .style("color","white")
                    .style("left", (d3.event.offsetX-40) + "px")
                    .style("top", (d3.event.offsetY + 10) + "px");
            })
            .on("mouseout",function (d) {
                tooltips.style("opacity", 0.0);
            });
    }