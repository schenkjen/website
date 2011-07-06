/**
 * @author Eric
 */

MooEditable.UI.PhotosearchDialog = function(editor){
	var html = 'search <input id="photosearch" class="search-input" value="" size="15"/> '
			+ 'align <select><option value="fr">Right</option><option value="fl">Left</option></select> '	
			+ '<button class="dialog-button dialog-ok-button">OK</button> '
			+ '<button class="dialog-button dialog-cancel-button">Cancel</button> ';
	var imagesearch, imageElement, photoinput, photourl;
	return new MooEditable.UI.Dialog(html,{
		'class':'mooeditable-prompt-dialog',
		onOpen:function(){
			photoinput = $('photosearch');
			//photourl = $('photourl');
			imagesearch = new Autocompleter.Request.JSON(photoinput.id, '/search/photos/',{
			'selectMode': 'pick',
			postVar:'search',
		      injectChoice: function(token){
		      	var choice = new Element('li',{
						events:{
							click:function(e){
								//photoinput.store('image', );
								photoinput.value='';
								photoinput.set('value',token.image);
								
							}
						}
					});
					new Element('img',{
						src:token.preview,
						'class':'fl'
					}).inject(choice);
					new Element('div',{
						text:token.title
					}).inject(choice);
					new Element('br', {
						'class':'clearfloat'
					}).inject(choice);
		            this.addChoiceEvents(choice).inject(this.choices);
		        }
			});
			Log.log("OPEN!", photoinput);
		},
		onClose:function(e){
			imagesearch.destroy();
		},
		onClick:function(e){
			if (e.target.tagName.toLowerCase() == 'button') e.preventDefault();
			var button = document.id(e.target);
			if (button.hasClass('dialog-cancel-button')) {
				this.close();
				Log.log("cancel");
				photoinput.value = "";
			}
			else 
				if (button.hasClass('dialog-ok-button')) {
					this.close();
					if (photoinput.value !== ""){
						var wrap = new Element('div');
						imageElement = new Element('img',{
							src:photoinput.value,
							'class':'p_all-6 ' + this.el.getElement('select').value
						}).inject(wrap);
						Log.log('ok', photoinput.value);
						editor.selection.insertContent(wrap.get('html'));
						photoinput.value = "";
					}
				}
			
		}
	});
};
MooEditable.Actions.photosearch={
	title:'Find Image',
	type:'button',
	options:{
		mode:'icon',
		shortcut:'e'
	},
	dialogs:{
		prompt:function(editor){
			return MooEditable.UI.PhotosearchDialog(editor);
		}
	},
	command:function(){
		this.dialogs.photosearch.prompt.open();
	}
	
};
