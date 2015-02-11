var message_recieved = function(type, msg) {
    if(type == 'populate home table'){
	var rows = JSON.parse(msg);
	$table = $('#mainTable').bootstrapTable({data: rows });
	$table.bootstrapTable('load', rows);
	$table.on('click-row.bs.table', gotoLoan);

	for(var row in rows){
	    var r = rows[row];
	    if(parseInt(r.loanNum.slice(1)) > loanNum){
		loanNum = parseInt(r.loanNum.slice(1));
	    }
	}
	resetAddLoanForm();
    } else if(type == 'show loan info'){
	showLoan(JSON.parse(msg));
    } else if(type == 'show report') {
	$('#report').html('<pre>'+msg.replace(/"/g,'')+'</pre>');
    }
};

var showReceiptIcon = function(val, row){
    return '<a href="#"><i lnk="'+val+'" class="fa fa-newspaper-o recptClk icnBlue"></i></a>';
};


var paymentRow = '<tr><td><div class="input-group date" id="dateA%%" style="width:75%"><input id="date%%" type="text" class="form-control" data-date-format="YYYY-MM-DD"/><span class="input-group-addon"><span class="glyphicon glyphicon-calendar"></span></span></div></td> <td>$<input id="amount%%" name="amount%%" type="text" class="input"></td><td id="owed%">%Owed%%</td></tr>';
var rowNum = 0;
var curLoaned = 0;
var loanNum = 0;
var appFile = 0;
var recpt = 0;

var showHome = function(){
    $('#home').addClass('active');
    $('#add').removeClass('active');
    $('#reports').removeClass('active');
    $('#homeContent').show();
    $('#addLoan').hide();
    $('#loanProfile').hide();
    $('#report').hide();
};

var gotoLoan = function (e, row, $element) {
    loanNum = row.loanNum;
    // get loan information
    data = {loanNum: loanNum};
    data.message = 'Get Loan';
    send(JSON.stringify(data));
    // display loan information
    $('#loanProfile').show();
    $('#homeContent').hide();
};

var showLoan = function(loan) {
    loanInfo = loan.loan_info;
    $('#profName').text(loanInfo.name);
    $('#profDate').text(loanInfo.loan_date);
    $('#profApp').html('<a href="#" id="test">Something here soon...</a>');
    $('#profGen').text(loanInfo.gender);
    $('#profAmount').text(loanInfo.amount_loaned);
    $('#profNum').text(loanInfo.loan_number);
    $('#profAge').text(loanInfo.age);
    $('#profBusiness').text(loanInfo.business_type);
    $('#profLoc').text(loanInfo.location);
    $('#test').click(function(){
	$('#pdfIframe').modal('show');
        $('iframe').attr("src",'pdfjs/web/viewer.html?file='+loanInfo.application_file);
    });

    $table = $('#profSched').bootstrapTable({data: loan.schedule});
    $table.bootstrapTable('load', loan.schedule);
    $table.bootstrapTable('resetView', {height: (loan.schedule.length+1)*40});

    $table2 = $('#profPays').bootstrapTable({data: loan.payments});
    $table2.bootstrapTable('load', loan.payments);
    $table2.bootstrapTable('resetView', {height: (loan.payments.length+1)*40});

    $('.recptClk').click(function(e){
	$('#pdfIframe').modal('show');
        $('iframe').attr("src",'pdfjs/web/viewer.html?file='+$(this).attr('lnk'));
    });
};

$(function() {
    $('#loanDate').datetimepicker({
	pickTime: false
    });
    $('#loanDateF').datetimepicker({
	pickTime: false
    });

    $('#addLoan').hide();
    $('#loanProfile').hide();
    $('#home').click(showHome);
    $('#add').click(function(){
	$('#home').removeClass('active');
	$('#add').addClass('active');
	$('#reports').removeClass('active');
	$('#homeContent').hide();
	$('#addLoan').show();
	$('#loanProfile').hide();
	$('#report').hide();
    });
    $('#reports').click(function(){
	$('#home').removeClass('active');
	$('#add').removeClass('active');
	$('#reports').addClass('active');
	$('#addLoan').hide();
	$('#homeContent').hide();
	$('#loanProfile').hide();
	send(JSON.stringify({'message':'Get Report'}));
	$('#report').show();
    });
    $('#paymentdateD').datetimepicker({pickTime:false});
    $('#paymentDate').datetimepicker({pickTime:false});
    
    $('#amountLoaned').keyup(function(){
	curLoaned = parseInt($('#amountLoaned').val());
	recalcPaymentTable();
    });

    $('#addPaymentRow').click(function(){
	var pr = paymentRow + '';
	pr = pr.replace(/date%%/g, 'date'+rowNum);
	pr = pr.replace(/dateA%%/g, 'dateA'+rowNum);
	pr = pr.replace(/amount%%/g, 'amount'+rowNum);
	pr = pr.replace('%Owed%%', '$'+curLoaned);
	pr = pr.replace('owed%', 'owed'+rowNum);
	$('#paymentTableBody').append(pr);
	$('#amount'+rowNum).keyup(recalcPaymentTable);
	$('#amount'+rowNum).val('0');
	$('#date'+rowNum).datetimepicker({
	    pickTime: false
	});
	$('#dateA'+rowNum).datetimepicker({
	    pickTime: false
	});
	rowNum += 1;
	recalcPaymentTable();
    });

    $('#profAddPayment').click(function(){
	// open modal
	$('#addPaymentModal').modal('show');
	// save data
	// reload table
    });
    $('#savePay').click(function(){
	$('#addPaymentModal').modal('hide');
	var data = {};
	data.loanNum = loanNum;
	data.amount = $('#amountPaid').val();
	data.reciept = recpt;
	data.date = $('#paymentDate').val();

	$('#amountPaid').val('');
	$('#recpt').val('');
	$('#paymentDate').val('');

	data.message = 'Add Payment';
	send(JSON.stringify(data));
    });
    $('.closeP').click(function(){
	$('#amountPaid').val('');
	$('#recpt').val('');
	$('#paymentDate').val('');
    });
    $('#recpt').change(function(e){
	var input = e.target;
	var reader = new FileReader();
	reader.onloadend = function(e){
	    recpt = reader.result;
	};
	reader.readAsDataURL(input.files[0]);
    });


    $('#app').change(function(e){	
	var input = e.target;
	var reader = new FileReader();

	reader.onloadend = function(e){
	    appFile = reader.result;
	};
	reader.readAsDataURL(input.files[0]);
    });
    
    $('#saveLoan').click(function(){
	var data = {};
	data.name = $('#appName').val();
	data.file = appFile;
	data.loanDate = $('#loanDate').val();
	data.loanNum = $('#loanNum').val();
	data.amount = $('#amountLoaned').val();
	data.age = $('#age').val();
	data.gender = $("input:radio[name ='gender']:checked").val();
	data.business = $('#business').val();
	data.location = $('#loc').val();

	data.payments = [];
	for(var i = 0; i < rowNum; i++){
	    data.payments.push({date:$('#date'+i).val(), amount:$('#amount'+i).val()});
	}

	data.message = 'Add Loan';
	showHome();
	send(JSON.stringify(data));
	resetAddLoanForm();
    });
});

var recalcPaymentTable = function(){
    var tmp = curLoaned;
    for(var i = 0; i < rowNum; i++){
	tmp -= parseInt($('#amount'+i).val());
	$('#owed'+i).html('$'+tmp);
    }
};

function pad(v){
    v = v.toString();
    while(v.length < 4){
	v = '0'+v;
    }
    return v;
}

function resetAddLoanForm(){
    rowNum = 0;
    curLoaned = 0;
    $('#paymentTableBody').html('');
    $('#addLoanForm').trigger('reset');
    $('#loanNum').val('L'+pad(loanNum+1));
    $('#loanDate').val((new Date()).yyyymmdd());
}


function send(msg) {
    document.title = "null";
    document.title = msg;
}

Date.prototype.yyyymmdd = function() {
     var yyyy = this.getFullYear().toString();
     var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
     var dd  = this.getDate().toString();
     return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]); // padding
 };



var BASE64_MARKER = ';base64,';

var convertDataURIToBinary = function(dataURI) {
  var base64Index = dataURI.indexOf(BASE64_MARKER) + BASE64_MARKER.length;
  var base64 = dataURI.substring(base64Index);
  var raw = window.atob(base64);
  var rawLength = raw.length;
  var array = new Uint8Array(new ArrayBuffer(rawLength));

  for(i = 0; i < rawLength; i++) {
    array[i] = raw.charCodeAt(i);
  }
  return array;
}
