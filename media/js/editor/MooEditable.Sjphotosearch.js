MooEditable.UI.SjphotosearchDialog = function(editor){
	var html = 'url<input type="text" id="plainurl" value="" size="20" class="search-input"> '
			 + 'or search <input type="text" id="sjphotosearch" value="" size="20" class="search-input"/> '
			 + '<button class="dialog-ok-button">OK</button>'
			 + '<button class="dialog-cancel-button">Cancel</button>';
	var sitesearch, searchinput, urlinput;
	return new MooEditable.UI.Dialog(html,{
		'class':'mooeditable-prompt-dialog',
		onOpen:function(e){
			searchinput = $('sjphotosearch');
			urlinput = $('plainurl');
			sitesearch = new Autocompleter.Request.JSON(searchinput.id, '/search/',{
				postVar:'searchVal',
				minLength: 2,
				injectChoice:function(token){
					var choice = new Element('li',{
						events:{
							'click':function(e){
								urlinput.value=token.url;
								Log.log('click');
							}
						}
					});
					new Element('div', {
						html:this.markQueryValue(token.displayname),
						'class':'compact-text'
					}).inject(choice);
					new Element('div',{
						'class':'small',
						text:token.ct
					}).inject(choice);
					//new Element('br',{'class':'clearfloat'}).inject(choice);
					this.addChoiceEvents(choice).inject(this.choices);
				}
			});
		},
		onClose:function(e){
			sitesearch.destroy();
		},
		onClick:function(e){
			if (e.target.tagName.toLowerCase() == 'button') {
				e.preventDefault();
			}
			var button = document.id(e.target);
			if (button.hasClass('dialog-cancel-button')) {
				this.close();
				Log.log("cancel");
			}
			else 
				if (button.hasClass('dialog-ok-button')) {
					this.close();
					if (urlinput.value !== '') {
						var txt = editor.selection.getText();
						var link_wrap= new Element('div');
						new Element('a',{
							href:urlinput.value,
							text:txt
						}).inject(link_wrap);
						Log.log('ok', urlinput.value);
						editor.selection.insertContent(link_wrap.get('html'));
					}
				}			
			urlinput.value = "";			
		}
	});
	
};
MooEditable.Actions.sjphotosearch={
	title:'Find URL',
	type:'button',
	options:{
		mode:'icon',
		shortcut:'h'
	},
	dialogs:{	
		alert: MooEditable.UI.AlertDialog.pass('Please select the text you wish to hyperlink.'),
		prompt:function(editor){
			return MooEditable.UI.SjphotosearchDialog(editor);
		}
	},
	command:function(){
		if (this.selection.isCollapsed()) {
			this.dialogs.sjphotosearch.alert.open();
		}
		else {
			this.dialogs.sjphotosearch.prompt.open();
		}
	}
	
};
