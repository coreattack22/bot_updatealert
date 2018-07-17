//gasに配置するファイル参考

function push(){
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName("巡回対象");
    const range = sheet.getRange("C6:D100");
    const values = range.getValues().filter( function( value ) {
        return value[0] !='';
    })
    const id=sheet.getRange("C3").getValue();
    Logger.log(id);
  
    
   
    values.forEach(function(value) {
      const site_url=value[1].toString().split('/').join('-');
  
      if (value[0].toString()=='ライブドアブログ'){
        const url = "https://shareshortbot.herokuapp.com/push_update/"+site_url+"/"+id;  
      } else if (value[0].toString()=='wantedly') {
        console.log("作成中")
      }
      const response = UrlFetchApp.fetch(url);
      const content = response.getContentText("UTF-8");
    });
    
  }