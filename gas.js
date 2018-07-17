//gasに配置するファイル参考

function push(){
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName("巡回対象");
  const range = sheet.getRange("C6:D100");
  const values = range.getValues().filter( function( value ) {
      return value[0] !='';
  })
  const id=sheet.getRange("C3").getValue();

  
  values.forEach(function(value) {
    var site_url=value[1].toString().split('/').join('-');
    site_url=site_url.split('?').join('~');
    var url="";
    if (value[0].toString()=='ライブドアブログ'){
      url = "https://shareshortbot.herokuapp.com/push_livedoorblog/"+site_url+"/"+id;  
    } else if (value[0].toString()=='wantedly') {
      url = "https://shareshortbot.herokuapp.com/push_wantedly/"+site_url+"/"+id;  
    }
    UrlFetchApp.fetch(url).getContentText("UTF-8");
  });
  
}