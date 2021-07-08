// $(document).ready(function(){
//   $("#btn").click(function(){
//     $("#collapseExample").append(" <b>Appended text</b>.");
//   });
// });

counter = 1;
$(document).ready(function(){
  $("#btn").click(function(){
    var row = '<div class="row">';
    row += '<span class="col-sm-3 text-right">装置名:</span>';
    row += '<select class="ml-0" name=';
    row += "device" + counter;
    row += '><option>選択してください</option><option>CPU</option><option>Monitor</option></select>';
    row += '<span class="ml-3"> 開始日:</span>';
    row += '<input class="ml-2" type="date" name=';
    row += "start_date" + counter;
    row += ' value="">';
    row += '<span class="ml-3"> 終了日:</span>';
    row += '<input class="ml-2" type="date" name=';
    row += "end_date" + counter;
    row += ' value="">';
    row += '</div>';
    $("#collapseExample").append(row);
    counter ++;
  })
});
