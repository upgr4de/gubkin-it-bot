// Steven Schmatz
// Humanitas Labs
// 13 October, 2016

// Emil Aflatunov
// gublin-it
// April, 2021

// Sample form_url. Note that this must be authenticated with the current user
// var form_url = 'https://docs.google.com/forms/d/1TfDoYf8EuLWPWvHZHkegaKEUqkAgeYzB3CGeWQUVT68/edit';
// var answers = ['nvshdbvshdbvhsdbvhbsdvhsbhvbsbvhsdbvsdvs', 'gbcvbcvbcv', '', [], 'Вариант 1'];

/**
 * Converts the given form form_url into a JSON object
 */
function readForm(form_url) {
  var form = FormApp.openByUrl(form_url);
  var items = form.getItems();
  
  var result = {
    'metadata': getFormMetadata(form),
    'items': items.map(itemToObject)
  };

  // Logger.log(JSON.stringify(result));

  return result;
}

function writeForm(form_url, answers) {
  var form = FormApp.openByUrl(form_url);
  var items = form.getItems();
  var formResponse = form.createResponse();
  var j = 0;

  for (var i = 0; i < items.length; i++) {
    var item = items[i];

    switch (item.getType()) {
      case FormApp.ItemType.TEXT:
        item = item.asTextItem();
        break;
      case FormApp.ItemType.PARAGRAPH_TEXT: 
        item = item.asParagraphTextItem();
        break;
      case FormApp.ItemType.LIST: 
        item = item.asListItem();
        break;
      case FormApp.ItemType.MULTIPLE_CHOICE:
        item = item.asMultipleChoiceItem();
        break;
      case FormApp.ItemType.CHECKBOX:
        item = item.asCheckboxItem();
        break;
      default:
        continue;
    }

    if (answers[j] != '') {
      var itemResponse = item.createResponse(answers[j]);

      formResponse.withItemResponse(itemResponse);
    }

    j++;
  }

  formResponse.submit();
}

/**
 * Returns the form metadata object for the given Form object
 * @param form: Form
 * @returns (Object) object of form metadata
 */
function getFormMetadata(form) {
  return {
    'title': form.getTitle(),
    'id': form.getId(),
    'description': form.getDescription(),
    'editUrl': form.getEditUrl(),
    'publishedUrl': form.getPublishedUrl(),
    'editorEmails': form.getEditors().map(function(user) {return user.getEmail()}),
    'count': form.getItems().length,
    'confirmationMessage': form.getConfirmationMessage(),
    'customClosedFormMessage': form.getCustomClosedFormMessage()
  };
}

/**
 * Returns an Object for a given Item
 * @param item: Item
 * @returns (Object) object for the given item
 */
function itemToObject(item) {
  var data = {};
  
  data.type = item.getType().toString();
  data.title = item.getTitle();
  
  // Downcast items to access type-specific properties
  var itemTypeConstructorName = snakeCaseToCamelCase('AS_' + item.getType().toString() + '_ITEM');  
  var typedItem = item[itemTypeConstructorName]();
  
  // Keys with a prefix of 'get' have 'get' stripped
  var getKeysRaw = Object.keys(typedItem).filter(function(s) {return s.indexOf('get') == 0});
  
  getKeysRaw.map(function(getKey) {    
    var propName = getKey[3].toLowerCase() + getKey.substr(4);
    
    // Image data, choices, and type come in the form of objects / enums
    if (['image', 'choices', 'type', 'alignment'].indexOf(propName) != -1) {return};
    
    // Skip feedback-related keys
    if ('getFeedbackForIncorrect'.equals(getKey) || 'getFeedbackForCorrect'.equals(getKey)
      || 'getGeneralFeedback'.equals(getKey)) {return};
    
    var propValue = typedItem[getKey]();
    
    data[propName] = propValue;
  });
  
  // Bool keys are included as-is
  var boolKeys = Object.keys(typedItem).filter(function(s) {
    return (s.indexOf('is') == 0) || (s.indexOf('has') == 0) || (s.indexOf('includes') == 0);
  });
  
  boolKeys.map(function(boolKey) {
    var propName = boolKey;
    var propValue = typedItem[boolKey]();
    data[propName] = propValue;
  });
  
  // Handle image data and list choices
  switch (item.getType()) {
    case FormApp.ItemType.LIST:
    case FormApp.ItemType.CHECKBOX:
    case FormApp.ItemType.MULTIPLE_CHOICE:
      data.choices = typedItem.getChoices().map(function(choice) {
        return choice.getValue();
      });
      break;
    
    case FormApp.ItemType.IMAGE:
      data.alignment = typedItem.getAlignment().toString();
      
      if (item.getType() == FormApp.ItemType.VIDEO) {
        return;
      }
      
      var imageBlob = typedItem.getImage();
      
      data.imageBlob = {
        'dataAsString': imageBlob.getDataAsString(),
        'name': imageBlob.getName(),
        'isGoogleType': imageBlob.isGoogleType()
      };
      
      break;
      
    case FormApp.ItemType.PAGE_BREAK:
      data.pageNavigationType = typedItem.getPageNavigationType().toString();
      break;
      
    default:
      break;
  }
  
  // Have to do this because for some reason Google Scripts API doesn't have a
  // native VIDEO type
  if (item.getType().toString() === 'VIDEO') {
    data.alignment = typedItem.getAlignment().toString();
  }
  
  return data;
}

/**
 * Converts a SNAKE_CASE string to a camelCase string
 * @param s: string in snake_case
 * @returns (string) the camelCase version of that string
 */
function snakeCaseToCamelCase(s) {
  return s.toLowerCase().replace(/(\_\w)/g, function(m) {return m[1].toUpperCase();});
}