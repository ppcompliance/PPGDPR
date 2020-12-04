function GetComplineKey(data){
    var data = data;
    var keywords =[];
        var data_weight=[];
        // var com_could=[];
        for(var i=0;i<data.length;i++){
            var words = data[i].word;
            var weight = data[i].weight;
            // keywords.push(words);
            // data_weight.push(weight);
            if(weight>0.65){
                var keyword =words;
                // console.log(keyword);
                keywords.push(words);
                data_weight.push(weight);
            }

        }
        // console.log(keywords);

        annotate_keywords(keywords,data_weight)

}
function annotate_keywords(keywords,data_weight) {
        $(".center_text").each(function () {
            $(this).find('span').each(function () {
                var tmp = $(this).text();
                // console.log(tmp);
                var bb = keywords;
                // console.log(bb);

                for (var i = 0; i < bb.length; i++) {
                    var KeyWord =bb[i];
                    var reg = new RegExp("(\\b" + KeyWord + "\\b)");
                    // console.log(reg);
                    tmp = tmp.replace(reg, "<span class='keyword' >$1</span>");
                    $(this).html(tmp + "<br>");

                }
            })
            // document.getElementById("text").innerHTML=result;

        })
        var data_weight=data_weight;
        // console.log(data_weight);
        var color1='#0A6379',color2='#059EB8';
        var color = d3.scale.linear().domain([0,d3.max(data_weight)]).range([color1,color2]);
        var tooltips = d3.select("#OverviewText").append("div").attr("class", "tooltip").attr("opacity", 0.0);
        var svg = d3.selectAll('.keyword').data(keywords).attr("weight", function (d,i) {
            return data_weight[i];
        });
        var svg1 = d3.selectAll('.keyword').style("background",function(d){
            return color(d3.select(this).attr("weight"));
            console.log(d3.select(this).attr("weight"));
        }).on("mouseover",function (d) {
            var label_type = $(this).parent().attr("label");
            var app_label = ["收集个人数据","数据存储期限",  "收集数据目的", "联系方式", "访问数据权", "擦除或更改权", "限制处理权", "拒绝处理权", "数据携带权", "申诉权"];
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
                console.log(1111);
            });


    }




