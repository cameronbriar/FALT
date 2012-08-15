var oopts = {
  //textFont: 'Helvetica Neue,Helvetica,Arial,sans-serif',
  textFont: 'Arial, sans-serif',
  textHeight: 16,
  maxSpeed: 0.05,
  textColour: '#000',
  decel: 0.9,
  depth: 0.99,
  reverse: true,
  outlineColour: '#366DDC',
  outlineThickness: 3,
  pulsateTo: 0.2,
  pulsateTime: 0.5,
  wheelZoom: true,
  initial: [0.1, -0.1]
}, ttags = 'taglist', lock, shape = 'sphere';

  window.onload = function() {
      $("#eCanvas").tagcanvas(oopts);
      oopts["initial"] = [-0.1, 0.1];
      $("#iCanvas").tagcanvas(oopts);
  };
function handleFileSelect(evt) {
        var file = evt.target.files;
        //must be a txt file
        if (!(file[0].type == 'text/plain')) {
          postStatus("Error", "<h3 style='color:white'>Error</br>Filetype must be <u>.txt</u></h3>", "important", 8000);
          return;
        }
        //must be less than 10Kb
        if (file[0].size > 10000) {
          postStatus("Error", "<h3 style='color:white'>Error</br>Filesize must be <u>less than 10Kb</u></h3>", "important", 8000);
          return;
        }
        for (var i = 0, f; f = file[i]; i++) {
          var reader = new FileReader();
          reader.onload = (function(theFile) {
            return function(e) {
              $("#fileClose").removeAttr("disabled");
              postStatus("Success", "<h3 style='color:white'>Success</br>File uploaded!</h3>", "success", 6000);
              var content = formatContent(e.target.result);
            };
          })(f);
          reader.readAsText(f, "UTF-8");
        }
      }
      document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);

function formatContent(content) {
  var listWords = new Array();
   listWords[0] = content.split(',');
   listWords[1] = content.split('\n');
   listWords[2] = content.split(' ');
   var wordList = maxArrayOfArray(listWords).join(" ");
   //var wordList = listWords[1].join(" ");
   $("#wordSubmit").val(wordList);
   console.log(wordList);
   $("#wordAdd").click();
  return;
}
function addWord(word) { 
  $("#wordSubmit").val(word);
  $("#wordAdd").click();
}
$("#addSim").live({click : function(){addWord($(this).html());}});
$("span#viseme").live({click : function(){toggleClass($(this).html());}});
  function maxArrayOfArray(arr) {
    var max = 0;
    var index, i = 0;
    for (x in arr) {
      if (arr[x].length > max) {
        max = arr[x].length;
        index = i;
      } i += 1;
    }
    var dets = "Max:" + max.toString();
    return arr[index];  
  }
	//Initializers
var isMobile = {
    Android: function() {
        return navigator.userAgent.match(/Android/i) ? true : false;
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i) ? true : false;
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i) ? true : false;
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i) ? true : false;
    },
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Windows());
    }
};

var deviceType = 'large';

if ( isMobile.any() ) {
  deviceType = 'small';
  document.addEventListener("touchstart", touchHandler, true);
  document.addEventListener("touchmove", touchHandler, true);
  document.addEventListener("touchend", touchHandler, true);
  document.addEventListener("touchcancel", touchHandler, true); 
} else {
  welcomeInto();
}
  $(".centered").css("text-align", "center")
  $("h2#loading").hide();
  $("#externalCanvas").hide();
  $("#internalCanvas").hide();
  $("h6#fileInputNotSupported").hide();
  $("div#fileInputContainer").hide();
  $("tr#hoverMore").popover({'placement': 'bottom', 'animate' : 'false', 'title' : 'Audiovisual', 'trigger' : 'manual', 'content' : ''});

  $("#aboutDelimiter").tooltip();
  $("#fileLoading").hide();

  $('input[id=fileInput]').change(function() {
  $('#fakeFile').val($(this).val().replace("C:\\fakepath\\", "")); });
  var lecChoices = '<div class="btn-toolbar"><div id="presets" class="btn-group"><button id="preset" class="btn btn-primary" style="cursor:pointer">0</button><button id="preset" class="btn btn-primary" style="cursor:pointer">1</button><button id="preset" class="btn btn-primary" style="cursor:pointer">2</button><button id="preset" class="btn btn-primary" style="cursor:pointer">10</button><button id="preset" class="btn btn-primary" style="cursor:pointer">12</button><button id="preset" class="btn btn-primary" style="cursor:pointer">19</button><button id="preset" class="btn btn-primary" style="cursor:pointer">28</button></div></div>';

var data = new Array();
data.currentClass = 1;
data.isVisible = false;
data.currentSymbol = "&lt;";
data.currentWord = 'fresno audio visual lexy con tool'; // sounds better this way
data.myWords = new Array();
data.popLocked = false;
data.distance = 1;
data.equivalenceClasses = new Array();
data.equivalenceClasses[0] = 0;
data[0] = 0;
data[1] = 'crosshatch,&#9641;';
data[2] = 'snowman,&#9731;';
data[3] = 'at,&#64;';
data[4] = 'female,&#9792;';
data[5] = 'scissors,&#9988;';
data[6] = 'airplane,&#9992;';
data[7] = 'cloud,&#9729;';
data[8] = 'fourpoint,&#10022;';
data[9] = 'flower,&#10047;';
data[10] = 'phonemic,&#9742;';
data[11] = 'sun,&#10050;';
data[12] = 'peace,&#9996;';
data[13] = 'blackstar,&#10040;';
data[14] = 'elevator,&#10208;';
data[15] = 'chess,&#9818;';
data[16] = 'smile,&#9786;';
data[17] = 'circle,&#10687;';
data[18] = 'wheel,&#9784;';
data[19] = 'pencil,&#9998;';
data[20] = 'coffee,&#9832;';
data[21] = 'umbrella,&#9730;';
data[22] = 'perceive,&#9717;';
data[23] = 'mac,&#8984;';
data[24] = 'eject,&#9167;';
data[25] = 'medical,&#9764;';
data[26] = 'biohazard,&#9763;';
data[27] = 'blackdiamond,&#10070;';
data[28] = 'castle,&#9814;';
data[29] = 'star,&#9733;';
data[30] = 'sagit,&#9808;';

data.equivalencePresets = new Array();
data.equivalencePresets[28] = 
  [ ['ʊ'], ['u'], ['eɪ', 'ɝ'], ['oʊ'], ['aʊ'], ['ɪ', 'i'], ['ɛ'], ['æ'], ['ɔɪ'], ['ɔ'], ['aɪ'], ['ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l'], ['n'], ['k'], ['ɡ', 'ŋ'], ['h'], ['d'], ['t'], ['s', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ'], ['tʃ'], ['ʒ'], ['dʒ']];
data.equivalencePresets[19] = 
[ ['ʊ', 'u', 'eɪ', 'ɝ'], ['oʊ', 'aʊ'], ['ɪ', 'i'], ['ɛ'], ['æ'], ['ɔɪ'], ['ɔ'], ['aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l'], ['n', 'k'], ['ɡ', 'ŋ'], ['h'], ['d'], ['t', 's', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ', 'tʃ', 'ʒ', 'dʒ']];
data.equivalencePresets[12] = 
[ ['ʊ', 'u', 'eɪ', 'ɝ'], ['oʊ', 'aʊ'], ['ɪ', 'i', 'ɛ','æ'], ['ɔɪ'], ['ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l','n', 'k','ɡ', 'ŋ','h'], ['d','t', 's', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ', 'tʃ', 'ʒ', 'dʒ']];
data.equivalencePresets[10] = 
[ ['ʊ', 'u', 'eɪ', 'ɝ'], ['oʊ', 'aʊ'], ['ɪ', 'i', 'ɛ','æ'], ['ɔɪ' ,'ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm'], ['v', 'f'], ['l', 'n', 'k', 'ɡ', 'ŋ', 'h', 'd', 't', 's', 'z'], ['r', 'w'], ['ð', 'θ'], ['ʃ', 'tʃ', 'ʒ', 'dʒ']];
data.equivalencePresets[2] =  
[ ['ʊ', 'u', 'eɪ', 'ɝ', 'oʊ', 'aʊ', 'ɪ', 'i', 'ɛ','æ', 'ɔɪ' ,'ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j'], ['p', 'b', 'm', 'v', 'f', 'l', 'n', 'k', 'ɡ', 'ŋ', 'h', 'd', 't', 's', 'z', 'r', 'w', 'ð', 'θ', 'ʃ', 'tʃ', 'ʒ', 'dʒ']];
data.equivalencePresets[1] =  
[ ['ʊ', 'u', 'eɪ', 'ɝ', 'oʊ', 'aʊ', 'ɪ', 'i', 'ɛ','æ', 'ɔɪ' ,'ɔ', 'aɪ', 'ʌ', 'ə', 'ɑ', 'j', 'p', 'b', 'm', 'v', 'f', 'l', 'n', 'k', 'ɡ', 'ŋ', 'h', 'd', 't', 's', 'z', 'r', 'w', 'ð', 'θ', 'ʃ', 'tʃ', 'ʒ', 'dʒ']];

data.equivalencePresetsARPA = new Array();
data.equivalencePresetsARPA[1] = [['UH', 'UW', 'EY', 'ER', 'OW', 'AW', 'IH', 'IY', 'EH', 'AE', 'OY', 'AO', 'AY', 'AH', 'AA', 'Y', 'P', 'B', 'M', 'V', 'F', 'L', 'N', 'K', 'G', 'NG', 'HH', 'D', 'T', 'S', 'Z', 'R', 'W', 'DH', 'TH', 'SH', 'CH', 'ZH', 'JH']];
data.equivalencePresetsARPA[2] = [['UH', 'UW', 'EY', 'ER', 'OW', 'AW', 'IH', 'IY', 'EH', 'AE', 'OY', 'AO', 'AY', 'AH', 'AA', 'Y'], ['P', 'B', 'M', 'V', 'F', 'L', 'N', 'K', 'G', 'NG', 'HH', 'D', 'T', 'S', 'Z', 'R', 'W', 'DH', 'TH', 'SH', 'CH', 'ZH', 'JH']];
data.equivalencePresetsARPA[10] = [['UH', 'UW', 'EY', 'ER'], ['OW', 'AW'], ['IH', 'IY', 'EH', 'AE'], ['OY', 'AO', 'AY', 'AH', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L', 'N', 'K', 'G', 'NG', 'HH', 'D', 'T', 'S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH', 'CH', 'ZH', 'JH']];
data.equivalencePresetsARPA[12] = [['UH', 'UW', 'EY', 'ER'], ['OW', 'AW'], ['IH', 'IY', 'EH', 'AE'], ['OY'], ['AO', 'AY', 'AH', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L', 'N', 'K', 'G', 'NG', 'HH'], ['D', 'T', 'S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH', 'CH', 'ZH', 'JH']];
data.equivalencePresetsARPA[19] = [['UH', 'UW', 'EY', 'ER'], ['OW', 'AW'], ['IH', 'IY'], ['EH'], ['AE'], ['OY'], ['AO'], ['AY', 'AH', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L'], ['N', 'K'], ['G', 'NG'], ['HH'], ['D'], ['T', 'S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH', 'CH', 'ZH', 'JH']];
data.equivalencePresetsARPA[28] = [['UH'], ['UW'], ['EY', 'ER'], ['OW'], ['AW'], ['IH', 'IY'], ['EH'], ['AE'], ['OY'], ['AO'], ['AY'], ['AH', 'AA', 'Y'], ['P', 'B', 'M'], ['V', 'F'], ['L'], ['N'], ['K'], ['G', 'NG'], ['HH'], ['D'], ['T'], ['S', 'Z'], ['R', 'W'], ['DH', 'TH'], ['SH'], ['CH'], ['ZH'], ['JH']];

Array.prototype.remove= function(){
    var what, a= arguments, L= a.length, ax;
    while(L && this.length){
        what= a[--L];
        while((ax= this.indexOf(what))!= -1){
            this.splice(ax, 1);
        }
    }
    return this;
}

	//Click Functions

	// Arrow Clicks
	$("#leftArrow").click(function() {
		var tracker = $("#equivClass").html();
		if (!(tracker <= 1) && !(tracker > 25))
			$("[id=equivClass]").each(function() { $(this).html(parseInt($(this).html()) - 6); });

	});
	$("#rightArrow").click(function() {
		var tracker = $("#equivClass").html();
		if (!(tracker < 1) && !(tracker > 24))
			$("[id=equivClass]").each(function() { $(this).html(parseInt($(this).html()) + 6); });
	});

	//Equivalence Class Group Click
	$("button#equivClass").click(function() {
		if ($(this).html() != String(data.currentClass)) {
		data.currentClass = $(this).html();
		$("th#classNum").html(data.currentClass);
		$("th#classSym").html(data[data.currentClass].split(",")[1]);

		$("span#grouped").html("");
		$("ul#eclass"+data.currentClass+" li button").each(function() {
			$("span#grouped").append($(this).clone());
		});
		}
	});

//Upload File Click
  $("#uploadFile").click(function() {
    if (!(isMobile.any()))
      $("div#fileInputContainer").toggle();
    else
      $("h6#fileInputNotSupported").toggle();
  })
	//Transcription Tab
	$('#phonetic a').click(function(e) {

		if (!($(this).parent().hasClass('active'))) {
		$("h2#transcription").hide();
		$("h2#loading").show()
  	e.preventDefault();
  	$(this).tab('show');
  	var t=setTimeout(function(){		
  		$("h2#transcription").show();
		$("h2#loading").hide()}, 2000);
	}});
	$('li#phonetic > a').click(function() {
    	$('li#phonetic').removeClass();
    	$(this).parent().addClass('active');
	});

  $("td#similar").live({
    click : function() {
      addWord($(this).val());
    }
  });

  $("#showInternals").click(function() {
    if (data.currentWord !='fresno audio visual lexy con tool') {
    var x = $("#mainWordInternalWords");
    x.html("");
    x.append("<table class='table table-striped' style='width:100%'>"+$("[value="+data.currentWord+"]").attr("internal")+"</table>");
  }
    return;
  });
  $("#showExternals").click(function() {
    if (data.currentWord !='fresno audio visual lexy con tool') {
    var x = $("#mainWordExternalWords");
    x.html("");
    x.append("<table class='table table-striped' style='width:100%'>"+$("[value="+data.currentWord+"]").attr("external")+"</table>");
  }
    return;
  });
	//Transcription Item
	$("button#phon").live({
		click : function() {
		data.classname = 'ul#eclass'+data.currentClass;
		data.currentPhoneme = $(this).html();
		data.currentCategory = $(this).attr('value');

		$(data.classname).append('<li id="'+data.currentPhoneme+'"><button id="phonActive" class="btn btn" value="'+data.currentCategory+'">'+data.currentPhoneme);

		$("span#grouped").append('<button id="phonActive" class="btn btn" value="'+data.currentCategory+'">'+data.currentPhoneme);
		$(this).remove();
		}
	});
	$("button#phonActive").live({
		click : function() {
		data.currentPhoneme = $(this).html();
		data.currentCategory = $(this).attr('value');
		$("li#"+data.currentPhoneme).remove();

		$("p."+data.currentCategory).append('<button id="phon" class="btn" value="'+data.currentCategory+'">'+data.currentPhoneme);
		$(this).remove();
    console.log("removing "+String(data.equivalenceClasses[data.currentClass])+" from "+String(data.currentClass));
    var indexToRemove = Number(data.currentClass);
    data.equivalenceClasses.splice(indexToRemove, 1);
		}
	});
	function classCount() {
		return $("ul.classStorage li").parent().length;
	}

	//Hover Functions

  $("tr#hoverMore").click(function(){
      if (data.isVisible) {
        if ($(this).html() == data.currentWord)
          var t = setTimeout(function(){togglePopover();}, 500);
        dismissPopover();
      }
      else {
        togglePopover();
      }
    });

    $("#mainWord").click(function(){
      if (data.currentWord != undefined)
        speak.play(data.currentWord, {speed : 100});
    });
	//Word Bank

  // hover & touchstart are the same
	$("li#wordBank").live({
		mouseover : function() {
      data.currentWord = $(this).html();
      $("#mainLogo").html(data.currentWord);
      $("#mainWordSymbolized").html($("[value = "+data.currentWord+"]").attr("symbol"));
  	  $("b#wordSyllables").html($("[value = "+data.currentWord+"]").attr("syllable-count"));
      $("b#wordFam").html($("[value = "+data.currentWord+"]").attr("familiarity"));

      $("#mainWordVisemes").html($("[value = "+data.currentWord+"]").attr("visemes"));
      $("#mainWordInternalCount").html($("[value = "+data.currentWord+"]").attr("internalCount"));
      $("#mainWordExternalCount").html($("[value = "+data.currentWord+"]").attr("externalCount"));
      $("#mainWordIPA").html($("[value = "+data.currentWord+"]").attr("ipa"));
      $("#mainWordARPA").html($("[value = "+data.currentWord+"]").attr("arpa"));
      $("#mainWordInternalFrequency").html($("[value = "+data.currentWord+"]").attr("internalfrequency"));
      $("#mainWordExternalFrequency").html($("[value = "+data.currentWord+"]").attr("externalfrequency"));
      $("#mainWordTotalFrequency").html($("[value = "+data.currentWord+"]").attr("totalfrequency"));
      $("#mainWordFrequency").html($("[value = "+data.currentWord+"]").attr("wordFrequency"));
      $("#mainWord").html($("[value = "+data.currentWord+"]").attr("dictionary"));
      $("#mainWordInternalWords").html("");
      $("#mainWordExternalWords").html("");

    $("#internalCloud").html("");
    var iwords = $("[value="+data.currentWord+"]").attr("internalCloud");
    if (iwords == '<li><a id="addSim" href="#"></a></li>')
      iwords = "<li><a href=\"#\">NONE</a></li>";
    $("#internalCloud").append(iwords);
    $("#iCanvas").tagcanvas(oopts);
    $("#internalCanvas").show();

    $("#externalCloud").html("");
    var ewords = $("[value="+data.currentWord+"]").attr("externalCloud");
    if (ewords == '<li><a id="addSim" href="#"></a></li>')
      ewords = "<li><a href=\"#\">NONE</a></li>";
    $("#externalCloud").append(ewords);
    $("#eCanvas").tagcanvas(oopts);
    $("#externalCanvas").show();

    //$("tr#hoverMore").attr('data-content', data.newContent);
    //$("tr#hoverMore").data('popover').options.content = data.newContent;
    //if (!data.popLocked)
      //$("tr#hoverMore").popover('show');
    //$("b#wordLEC1").html($($(this).html()).attr("syllable-count"));
		//console.log($("[value = "+data.currentWord+"]").attr("syllable-count"));
		},
		touchstart : function() {
      data.currentWord = $(this).html();
      $("#mainLogo").html(data.currentWord);
      $("#mainWordSymbolized").html($("[value = "+data.currentWord+"]").attr("symbol"));
      $("b#wordSyllables").html($("[value = "+data.currentWord+"]").attr("syllable-count"));
      $("b#wordFam").html($("[value = "+data.currentWord+"]").attr("familiarity"));

      $("#mainWordVisemes").html($("[value = "+data.currentWord+"]").attr("visemes"));
      $("#mainWordInternalCount").html($("[value = "+data.currentWord+"]").attr("internalCount"));
      $("#mainWordExternalCount").html($("[value = "+data.currentWord+"]").attr("externalCount"));
      $("#mainWordIPA").html($("[value = "+data.currentWord+"]").attr("ipa"));
      $("#mainWordARPA").html($("[value = "+data.currentWord+"]").attr("arpa"));
      $("#mainWordInternalFrequency").html($("[value = "+data.currentWord+"]").attr("internalfrequency"));
      $("#mainWordExternalFrequency").html($("[value = "+data.currentWord+"]").attr("externalfrequency"));
      $("#mainWordTotalFrequency").html($("[value = "+data.currentWord+"]").attr("totalfrequency"));
      $("#mainWordFrequency").html($("[value = "+data.currentWord+"]").attr("wordFrequency"));
      $("#mainWord").html($("[value = "+data.currentWord+"]").attr("dictionary"));
      $("#mainWordInternalWords").html("");
      $("#mainWordExternalWords").html("");

    $("#internalCloud").html("");
    var iwords = $("[value="+data.currentWord+"]").attr("internalCloud");
    if (iwords == '<li><a id="addSim" href="#"></a></li>')
      iwords = "<li><a href=\"#\">NONE</a></li>";
    $("#internalCloud").append(iwords);
    $("#iCanvas").tagcanvas(oopts);
    $("#internalCanvas").show();

    $("#externalCloud").html("");
    var ewords = $("[value="+data.currentWord+"]").attr("externalCloud");
    if (ewords == '<li><a id="addSim" href="#"></a></li>')
      ewords = "<li><a href=\"#\">NONE</a></li>";
    $("#externalCloud").append(ewords);
    $("#eCanvas").tagcanvas(oopts);
    $("#externalCanvas").show();

		},
    click : function() {
      $("#showInternals").click();
      $("#showExternals").click();
      if (data.isVisible) {
        if ($(this).html() == data.currentWord)
          var t = setTimeout(function(){togglePopover();}, 500);
        dismissPopover();
      }
      else {
        togglePopover();
      }
      data.popLocked = !data.popLocked;
    },
    dblclick : function() {
      removeWordBankWord($(this).html());
      dismissPopover();
      data.myWords.remove($(this).html());
    }
	});

  function wordBankCount(){
    return $("#newWords").children().length;
  }
  function removeWordBankWord(word) {
    $("li#wordBank").each(function(){if ($(this).html() == word) $(this).remove();})
    return;
  }
  function togglePopover() {
    $("tr#hoverMore").popover('show');
    data.isVisible = true;
    $("b#wordMore i").attr("class", "icon-chevron-up");
    return;
  }
  function dismissPopover() {
    $("tr#hoverMore").popover('hide');
    data.isVisible = false;
    $("b#wordMore i").attr("class", "icon-chevron-down");
    return;
  }
  $("#increase_modal").click(function(){
    var modal = $(this).attr("modal") + "_modal";
    var currentWidth = $("#"+modal).width();
    var newWidth = currentWidth + 300;
    var currentMargin = parseInt($("#"+modal).css("margin-left"));
    var newMargin = currentMargin - 150;
    $("#"+modal).width(newWidth).css("margin-left", String(newMargin)+"px");

    var currentHeight = $("#"+modal).height();
    var newHeight = currentHeight + 100;
    currentMargin = parseInt($("#"+modal).css("margin-top"));
    newMargin = currentMargin - 50;
    $("#"+modal).height(newHeight).css("margin-top", String(newMargin)+"px");
    return;
  });
	//Input Functions

	//Word Input
  // ****
	$("#newWord").submit(function(e) {
 		e.preventDefault();
		data.newWords = $("#wordSubmit").val().split(" ");
    if (data.newWords[0] == "") 
      if (wordBankCount != 0) {
        sendOff();
        return;
      }
      else 
        return;
		$("#wordSubmit").val('');
    data.wordCount = 0
		for (var i = 0; i < data.newWords.length; i++) {
      if (($.inArray(data.newWords[i], data.myWords)) == -1 && ($.inArray(data.newWords[i].toLowerCase(), data.myWords)) == -1) {
      //if (!(data.myWords.contains(data.newWords[i]))) {
          if (/^[a-zA-Z()]+$/.test(data.newWords[i])) {
        data.myWords.push(data.newWords[i].toLowerCase());
			 $("#newWords").append("<li id='wordBank' style='font-size:18px; padding:20px 0px 20px 0px;'>"+data.newWords[i].toLowerCase()+"</li>");
       data.wordCount += 1;
      }
        else {
          postStatus("Bad_Word", "<h4 style='color:white; padding-bottom:5px;'>Words must not contain symbols or numbers.</h4>", "important", 5000);
        }
      } 
    }
    postStatus("Words", "<h4 style='color:white; padding-bottom:5px;'>Added "+data.wordCount+" Word(s)</h4><h6 style='color:white; padding-bottom:5px'>Total: "+wordBankCount()+"</h6>", "success", 4000);
    sendOff("");
		$("#wordSubmit").focus();

	});

	//Status Updates
	function postStatus(itemname, message, type, time) {
	
		$("#status").append("<li id="+itemname+" class='label label-"+type+"' style='margin-top:3px'><strong>"+message+"</strong></li>"); 
		clearTextAt(itemname, time);
	} 
	function postStatusAt(itemname, message, type, time, delay) {

		var t=setTimeout(function(){postStatus(itemname, message, type, time);}, delay);
	} 
	function clearTextAt(itemname, when) {
	
		var t=setTimeout(function(){clearText(itemname)}, when);
	}
	
	function clearText(itemname) {
		//jQuery(('#'+itemname)).html("");
		jQuery(('#'+itemname)).remove();
	}
  function welcomeInto() {
	 postStatusAt("Welcome", "<h5 style='color:white; padding-bottom:5px;'>Welcome to</br>Fresno's Audiovisual</br>Lexicon Tool</h5>", "info", 3000, 2000);
	 postStatusAt("Welcome", "<h5 style='color:white; padding-bottom:5px;'>also known as</br><span style='font-size:32px'>FALT</span></h5>", "info", 3000, 6000);
  }

	//Keyboard Shortcuts

	//Gathering Data
	function getWordBank() {
		data.allWords = "";
		$("li#wordBank").each(function(){
			data.allWords = data.allWords + $(this).html() + ",";
		});
		data.allWords = data.allWords.substr(0, data.allWords.length-1);
		return data.allWords
	}

	function everything() {
		data.userClassNum = new Array();
	$(".classStorage").each(function() { 
		var i = $(this).children("li"); 
    data.className = getIntFrom($(this).attr("id"));
    console.log("Class --- "+data.className);
    data.userClassNum[data.className] = new Array();
		i.each(function(){
			$(this).children().each(function() {
      data.classPhoneme = $(this).html();
			data.userClassNum[data.className].push(data.classPhoneme);
			console.log(data.classPhoneme);
    });

	}); });
		return "Total Classes: "+totalClasses();
	}
function getIntFrom(theString) {
    rx=/(\d[\d\.\*]*)/g
    return theString.match(rx)[0];
}
function logClasses(){
return $(".classStorage").each(function() { var i = $(this).children("li"); i.each(function(){console.log($(this).children().html()+" at class "+getIntFrom($(this).parent().attr("id")))}); if (i.length) console.log("Size for this class = "+ i.length);});
}
function getEquivalenceClasses() {
	$(".classStorage").each(function() { 
		var i = $(this).children("li"); 
		if (i.length > 0) {
			data.equivalenceClasses[getIntFrom($(this).attr("id"))] = new Array();
			i.each(function(){
				var x = data.equivalenceClasses[getIntFrom($(this).parent().attr("id"))];
				x = ( typeof x != 'undefined' && x instanceof Array ) ? x : [];
			x.push($(this).children().html());
		}); 
		}
	});
	return data.equivalenceClasses; 
}
function getFormattedEquivalenceClasses() {
  var classes = getEquivalenceClasses();
  var returnString = '';
  var classCount = 0;
  for (var x = 1; x < classes.length; x += 1) {
    if (classes[x] == undefined)
      returnString = returnString + "|"
    else { 
      returnString = returnString + classes[x].join(",");
      returnString = returnString + "|"
      classCount += 1;
    }
  }
  returnString = returnString + classCount;
  return returnString;
}
function totalClasses() {
	return $(".classStorage li").parent().length;
}
function currentTranscriptionSelection() {
	return $("li#phonetic.active").children().html();
}
function currentClassSelection() {
  return Number($("th#classNum").html());
}
function currentClassKey() {
  return Number($("#equivClass").html());
}

// Presets

function togglePreset(presetNum) {
  if (presetNum == 0) toggleActivePhonemes(); 
  else { 
  if ($.inArray(presetNum, [1, 2, 10, 12, 19, 28]) != -1) {
    toggleTranscription('ipa');
    for (var i = 0; i < data.equivalencePresets[presetNum].length; i++) {
    //data.equivalencePresets[presetNum].each(function(index){ 
      toggleClass(i+1);
      for (var j = 0; j < data.equivalencePresets[presetNum][i].length; j++) {
        togglePhoneme(data.equivalencePresets[presetNum][i][j], 'ipa');
      }
    }
    toggleClass(1);
  } 
   else {
    postStatus("Preset", "<h4 style='color:white'>Presets Currently Available</h4><h5 style='color:white'>1 - 2 - 10 - 12 - 19 - 28</h5>", "inverse", 5000);
  } }
    return;
}
function togglePresetARPA(presetNum) {
  if (presetNum == 0) toggleActivePhonemes();
  else { 
  if ($.inArray(presetNum, [1, 2, 10, 12, 19, 28]) != -1) {
    toggleTranscription('arpa');
    for (var i = 0; i < data.equivalencePresetsARPA[presetNum].length; i++) {
      toggleClass(i+1);
      for (var j = 0; j < data.equivalencePresetsARPA[presetNum][i].length; j++) {
              togglePhoneme(data.equivalencePresetsARPA[presetNum][i][j], 'arpa');
      }
    }
    toggleClass(1);
  } 
  else {
    postStatus("Preset", "<h4 style='color:white'>Presets Currently Available</h4><h5 style='color:white'>1 - 2 - 10 - 12 - 19 - 28</h5>", "inverse", 5000);
  } }
  return;
}
function presetCount() {
  return Number($("span#amount").html());
}

$("button#preset").live({
  click : function() {
    data.preset = $(this).html();
    toggleActivePhonemes();
    slideTo(Number(data.preset));
    if (wordBankCount() != 0)
      sendOff();
  }});
$("button#betType").click(function() {
  toggleActivePhonemes();
    data.betSelection = $(this).html();
    data.currentClassCount = presetCount();
    switch (data.betSelection) {
      case 'ARPA':
      togglePresetARPA(data.currentClassCount);
      break;
      case 'IPA':
      togglePreset(data.currentClassCount);
      break;
      default:
      break;
    }
    return;
  });


//Iterating through the LEC
function toggleTranscription(betType) {
  betType = betType.toUpperCase();
  data.transcriptionSelection = ["IPA", "ARPA", "ALPHA"].indexOf(betType);
  if (!(data.transcriptionSelection == -1))
   $("li#phonetic").children().eq(data.transcriptionSelection).trigger("click")
  return;
}
function toggleClassPosition(classPos) { 
  return $("button#equivClass").eq((classPos-1)).trigger("click");
}
function toggleClass(classNum) {
  data.currentClass = currentClassSelection();
  if (data.currentClass == classNum || classNum < 1 || classNum > 30) return;
  data.currentClassKey = currentClassKey();
  data.classDifference = classNum - data.currentClassKey;
   if (Math.abs(data.classDifference) <= 5 && classNum >= data.currentClassKey)
      toggleClassPosition(data.classDifference+1);
   else {
      if (data.classDifference > 0)
        $("#rightArrow").trigger("click");
      else
        $("#leftArrow").trigger("click");
      toggleClass(classNum);
    }
    return;
  }
function toggleNextClass(direction) {
  switch (direction) {
    case '+':
    toggleClass(Number($("#classNum").html())+1);
    break;
    case '-':
    toggleClass(Number($("#classNum").html())-1);
    break;
    default:
    break;
  }
  return;
}
  function togglePhoneme(phoneme, betType) {
    var found = false;
    if (betType != 'ipa')
      phoneme = phoneme.toUpperCase();
    $("[value = "+betType+"]").each(function(){
      if ($(this).html() == phoneme) {
        $(this).trigger('click');
        found = true;
      }
    });
    if (!found)
      console.log("Did not find "+ phoneme);
    return;
    //$("[value = "+betType+"]:contains('"+phoneme+"')").trigger('click');
  }
  function toggleActivePhonemes() {
    $("button#phonActive").each(function(){$(this).trigger('click');});
    return;
  }
  function filterTranscription(transcriptionClass) {
    switch (transcriptionClass) {
      case 'arpa':
      $("button#phonActive").each(function(){ if ($(this).attr("value") == 'ipa' || $(this).attr("value") == 'alpha') $(this).trigger('click');});
      break;
      case 'ipa':
      $("button#phonActive").each(function(){ if ($(this).attr("value") == 'arpa' || $(this).attr("value") == 'alpha') $(this).trigger('click');});
      default:
      break;
  }
  return;
  }

	//Ajax
function sendOff(){

	data.dataToSend = getWordBank();
	data.dataSplit = data.dataToSend.split(",");
  data.currentClassSize = $("span#amount").html();
  if (data.currentClassSize == '0') {
     postStatus("Preset", "<h4 style='color:white'><a href='javascript:scrollBottom();' style='color:white;'><button class='btn'>Please choose LEC size.</button></a></h4>"+lecChoices, "important", 5000);
    return false;
  }
    var time1 = new Date();

    var urlToSend = 'main/';
    var dataToSend = 'words='+data.dataToSend+'&size='+data.currentClassSize+'&distance='+data.distance;
    var showResultsURL = urlToSend+"?"+dataToSend;

    $("#showResults").attr("href", showResultsURL);
    $("#mainWord").html('<small>Loading...</small>');
    postStatus("Loading", "<h2 style='color:white'>Loading</h2>", "info", 5000);
    $.ajax({
            type:"GET",
            url :urlToSend,
            data:dataToSend,
            datatype:"json",
            error:function(result){console.log("Please check your input and try again.");},//alert('There was an error.');},
            success:function(result){
              console.log(result);
              $("ul.wordStorage").html("");
            	for (var i = 0; i < data.dataSplit.length; i++) {
            		//console.log(result[data.dataSplit[i]]);
                //format similarities
                var intSims = result[data.dataSplit[i]].internal.split(" ");
                var extSims = result[data.dataSplit[i]].external.split(" ");
                var internalSimilars = new Array();
                var externalSimilars = new Array();
                var internalCloud = new Array();
                var externalCloud = new Array();
                for (var j = 0; j < intSims.length; j+=2) {
                  internalSimilars.push("<tr>"); 
                  internalSimilars.push("<td><span id=\"addSim\">");
                  internalSimilars.push(intSims[j])
                  internalSimilars.push("</span></td><td>");
                  internalSimilars.push(intSims[j+1])
                  internalSimilars.push("</td>");
                  internalSimilars.push("</tr>");

                  if (j < 100) {
                  internalCloud.push("<li><a id=\"addSim\" href=\"#\">");
                  internalCloud.push(intSims[j]);
                  internalCloud.push("</a></li>");
                  }
                }
                for (var j = 0; j < extSims.length; j+=2) {
                  externalSimilars.push("<tr>"); 
                  externalSimilars.push("<td><span id=\"addSim\">");
                  externalSimilars.push(extSims[j])
                  externalSimilars.push("</span></td><td>");
                  externalSimilars.push(extSims[j+1])
                  externalSimilars.push("</td>");
                  externalSimilars.push("</tr>");

                  if (j < 100) {
                  externalCloud.push("<li><a id=\"addSim\" href=\"#\">");
                  externalCloud.push(extSims[j]);
                  externalCloud.push("</a></li>");
                  }
                }
                var visemes = result[data.dataSplit[i]].visemes;
                visemes = visemes.split(" ");
                var formattedVisemes = new Array();
                for (var j = 0; j < visemes.length; j++) {
                  formattedVisemes.push("<span id=\"viseme\" style=\"cursor:pointer\">"+visemes[j]+"</span>");
                }
                visemes = formattedVisemes.join(" ");

            		$("ul.wordStorage").append("<li id='word"+i+"' value='"+data.dataSplit[i]+"' syllable-count='"+result[data.dataSplit[i]].syllables+"' symbol='"+result[data.dataSplit[i]].symbolized+"' wordFrequency='"+result[data.dataSplit[i]].wordFrequency+"' dictionary='"+result[data.dataSplit[i]].dictionary+"' ipa='"+result[data.dataSplit[i]].ipa+"' arpa='"+result[data.dataSplit[i]].arpa+"' visemes='"+visemes+"' internal='"+internalSimilars.join("")+"' external='"+externalSimilars.join("")+"' internalCount='"+result[data.dataSplit[i]].internalCount+"' externalCount='"+result[data.dataSplit[i]].externalCount+"' internalCloud='"+internalCloud.join("")+"' externalCloud='"+externalCloud.join("")+"' internalFrequency='"+result[data.dataSplit[i]].internalFrequency+"' externalFrequency='"+result[data.dataSplit[i]].externalFrequency+"' totalFrequency='"+result[data.dataSplit[i]].totalFrequency+"'></li>");
                $("#mainWord").html('<small>Loading Complete</small>');
            	}
                var time2 = new Date();
                console.log("Time to process "+ String(wordBankCount())+" words: "+String((time2.getTime() - time1.getTime())/1000));
                postStatus("Loading", "<h2 style='color:white'>Complete</h2>", "info", 3000);
            }
          });
    return false;
        }

//Keyboard Shortcuts

document.onkeyup = keyCheck;

function keyCheck(e) {
	
	var keyID = (window.event) ? event.keyCode : e.keyCode;
	if ($("#wordSubmit").is(":focus")){}else{
	switch(keyID) {
		case 80: // P
		if ($("#help_modal").is(".in"))
			$('#help_modal').modal('hide');
		else
			$('#help_modal').modal('show');
		break;
		case 83: // S
		if ($("#settings_modal").is(".in"))
			$('#settings_modal').modal('hide');
		else
			$('#settings_modal').modal('show');
		break;
    case 37: //Left Arrow
    toggleNextClass("-");
    break;
    case 39: //Right Arrow
    toggleNextClass("+");
    break;
    case 84: // T
    $("#changeStyle").click();
    break;
    case 75: // K
    if ($("#keyboard_modal").is(".in"))
      $('#keyboard_modal').modal('hide');
    else
      $('#keyboard_modal').modal('show');
    break;
    case 86: // V
    if ($("#symbols_modal").is(".in"))
      $('#symbols_modal').modal('hide');
    else
      $('#symbols_modal').modal('show');
    break;
    case 87: // W
    if ($("#welcome_modal").is(".in"))
      return;
    else
      return;
    break;
		default:
		break;
	}}
	return false;
}

// :)
function toggleHelp() {
	var e = {};
	e.keyCode = 80;
	keyCheck(e);
	return false;
}
function toggleSettings() {
	var e = {};
	e.keyCode = 77;
	keyCheck(e);
	return false;
}

// Touches (for slider)
// thanks to
// http://ross.posterous.com/2008/08/19/iphone-touch-events-in-javascript/
function touchHandler(event)
{
    var touches = event.changedTouches,
        first = touches[0],
        type = "";
         switch(event.type)
    {
        case "touchstart": type="mousedown"; break;
        case "touchmove":  type="mousemove"; break;        
        case "touchend":   type="mouseup"; break;
        default: return;
    }

             //initMouseEvent(type, canBubble, cancelable, view, clickCount, 
    //           screenX, screenY, clientX, clientY, ctrlKey, 
    //           altKey, shiftKey, metaKey, button, relatedTarget);
    
    var simulatedEvent = document.createEvent("MouseEvent");
    simulatedEvent.initMouseEvent(type, true, true, window, 1, 
                              first.screenX, first.screenY, 
                              first.clientX, first.clientY, false, 
                              false, false, false, 0/*left*/, null);

    first.target.dispatchEvent(simulatedEvent);
    //event.preventDefault();
}

function scrollTop() {
       $('html, body').animate({
         scrollTop: $(".navbar").offset().top
     }, 1500);
}
function scrollBottom() {
       $('html, body').animate({
         scrollTop: $("#presets").offset().top
     }, 1500);
}

  //Slider
  $("#slider").append( "<div id='slider-range-min'></div>" );
  function slideTo(pos) {
    if (pos >= 0 && pos <= 30) {
    $("#slider").html("");
    $("#slider").append( "<div id='slider-range-min'></div>" );
    $("#slider-range-min").slider({
      range: "min",
      value: pos,
      min: 0,
      max: 30,
      slide: function( event, ui ) {
        $( "#amount" ).html( ui.value );
        if ($.inArray(ui.value, [1,2,10,12,19,28]) != -1) {
          toggleActivePhonemes();
          togglePreset(ui.value);
        } else {
          if (ui.value == 0)
            toggleActivePhonemes();
        }
        return;
      }
  });
  $( "#amount" ).html( $( "#slider-range-min" ).slider( "value" ) );
    togglePreset(pos);
    }
  }
  slideTo(0);

$("#changeStyle").click(function(){
  var count = Number($("#changeStyle").attr("count"));
  count += 1;
  switch (count % 6) {
    case 0:
    document.getElementById('stylesheet').href = "/static/css/bootstrap.css";
    postStatus("StyleChange", "<h3 style='color:white'>Bootstrap</h3>", "info", 5000);
    break;
    case 1:
    document.getElementById('stylesheet').href = "/static/css/superhero/bootstrap.min.css";
    postStatus("StyleChange", "<h3 style='color:white'>Superhero</h3>", "info", 5000);
    break;
    case 2:
    document.getElementById('stylesheet').href = "/static/css/cerulean/bootstrap.min.css";
    postStatus("StyleChange", "<h3 style='color:white'>Cerulean</h3>", "info", 5000);
    break;
    case 3:
    document.getElementById('stylesheet').href = "/static/css/spacelab/bootstrap.min.css";
    postStatus("StyleChange", "<h3 style='color:white'>Space Lab</h3>", "info", 5000);
    break;
    case 4:
    document.getElementById('stylesheet').href = "/static/css/united/bootstrap.min.css";
    postStatus("StyleChange", "<h3 style='color:white'>United</h3>", "info", 5000);
    break;
    case 5:
    document.getElementById('stylesheet').href = "/static/css/simplex/bootstrap.min.css";
    postStatus("StyleChange", "<h3 style='color:white'>Simplex</h3>", "info", 5000);
    break;
    default:
    break;
  }
  $("#changeStyle").attr("count", count);
  return;
})
