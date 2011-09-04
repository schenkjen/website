/**
 * Copyright (C) 2008, 2009 Eric Satterwhite & The SJ Photography
 * 
 * All Rights Reserved
 * ATTRIBUTION ASSURANCE LICENSE (adapted from the original BSD license)
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the conditions below are met.
 * These conditions require a modest attribution to ERIC SATTEERWHITE (the
 * "SJ Photography"), who hopes that its promotional value may help justify the
 * thousands of dollars in otherwise billable time invested in writing
 * this and other freely available, open-source software.

 * 1. Redistributions of source code, in whole or part and with or without
 * modification (the "Code"), must prominently display this GPG-signed
 * text in verifiable form.
 * 2. Redistributions of the Code in binary form must be accompanied by
 * this GPG-signed text in any documentation and, each time the resulting
 * executable program or a program dependent thereon is launched, a
 * prominent display (e.g., splash screen or banner text) of the Author's
 * attribution information, which includes:
 * (a) Name ("ERIC SATTERWHITE"),
 * (b) Professional identification ("DIRECTOR OF WEBSITE OPERATIONS"), and
 * (c) URL ("sjphotography.com").
 * 3. Neither the name nor any trademark of the Author may be used to
 * endorse or promote products derived from this software without specific
 * prior written permission.
 * 4. Users are entirely responsible, to the exclusion of the Author and
 * any other persons, for compliance with (1) regulations set by owners or
 * administrators of employed equipment, (2) licensing terms of any other
 * software, and (3) local regulations regarding use, including those
 * regarding import, export, and use of encryption software.

 * THIS FREE SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 * FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
 * EVENT SHALL THE AUTHOR OR ANY CONTRIBUTOR BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * EFFECTS OF UNAUTHORIZED OR MALICIOUS NETWORK ACCESS;
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
 * IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 * --End of License
 */

/**
 * @license:	http://www.opensource.org/licenses/attribution.php Attribution Assurance License
 * @author:		Eric Satterwhite
 * 					-webmaster@sjphotography.com
 * 					-esatterwhite@wi.rr.com
 *
 * @version:	0.6
 * @credits:	Mootools(1.2.x)		
 * 					- A Compact Javasctipt framework that makes doin this kind of stuff less stressfull
 * 					http://www.mootools.net
 * 
 */

Class.Mutators.TrackInstances = function(track){
	if(!track) return;
	
	var oldInit = this.prototype.initialize;
	var klass = this;
	
	klass.prototype.initialize = function(){
		(klass.instances = klass.instances || []).push(this);
		oldInit.apply( this, arguments);	
	};
};
String.uniqueID = function(){
	return $time().toString(36)
};

(function(window){
	var SJPHOTO={
		version:'0.6',
		build:'3d9f8fd59fe3fdcf97d84f43f08edf2ada11b5be',
		author:'Eric Satterwhite'
	};
	SJPHOTO.Overlay = new Class({
		Implements:[Events, Options],
		/**
		 * 
		 * @param {String} bgColor: hex code of the color of the overlay
		 */
		options:{
			bgColor:'#000000',
			opacity:0.6,
			closeable:false,
			element:document.body,
			zindex:500,
	        loadClass: 'loader',						
		},
		element:null,
		isMaskOn: false,
		initialize:function(options){
			// set base options
			this.setOptions(options);
			this.baseIndex = this.options.zindex + SJPHOTO.Overlay.instances.length;
			// we use the number of instances to increase the z-index 
			// as new instances are created  			
			this.render();
			this.inject();
			this.position();
		},
		TrackInstances:true,
		render:function(){
			
			this.mask = new Element('div',{
				id:String.uniqueID(),
				styles: {
					position: 'fixed',
					height: '100%',
					width: '100%',
					'background-color': this.options.bgColor,
					opacity: 0,
					top:0,
					left:0,
					visibility:'hidden',
					'z-index': this.baseIndex

				},
				events: {
					dblclick: function(e){
						this.options.closeable ? this.hide() : false;
					}.bind(this)
				}				
			});			
		},
		position:function(){
			this.resize();
			this.mask.position({
				relativeTo:this.options.element,
				position:'topLeft'
			});			
		},
		inject:function(){
			this.mask.inject(this.options.element,'top');
		},		
		reveal:function( options ){
		  if(this.isMaskOn){
		    return this;
		  }
			if( options ){ 
				this.setOptions( options );
			}			
			
			this.isMaskOn = true;
			this.mask.fade(this.options.opacity);
			return this;
		},
		resize:function(x, y){
			dim = this.options.element.getComputedSize({
				styles:['padding', 'border']
			});
			
			this.mask.setStyles({
				width:$pick(x, dim.totalWidth, dim.x),
				height:$pick(y, dim.totalHeight, dim.y)
			});
		},
		/**
		 * 
		 */
		hide:function(){
			this.mask.fade('out');
			this.isMaskOn = false;
			return this;
		},
		/**
		 * 
		 */
		destroy:function(){
			try {
				SJPHOTO.Overlay.instances.erase(this);
			}catch(e){}
			this.mask.destroy();	
			this.mask= null;
		},
		toElement:function(){
			return this.mask;
		}		
	});
	SJPHOTO.LaunchPad = new Class({
	    /*
	     * Used to display modal windows/'pop-ups'
	     * This is an extension of the general utils.Overlay class.
	     * You can pass in all of the same options to customize the
	     * functionaliy of the overlay as well as the modalbox.
	     *
	     * Creating a new ModalBox creates & controls a new Overlay.
	     */
	    Implements: [Options, Events],
	    Extends: SJPHOTO.Overlay,
	    options: {
	        closeable: false,
	        modalBox: null, // element to inject into the 
	        title: null,
	        stage: null,
	        titleBar: null,
	        className: 'smallBox',
	        isMaskOn: false,
	        zindex:500
	        /*
			onBoxopen: $empty,
	        onBoxclose: $empty
	        */
	    
	    },
	    initialize: function(options){
	        this.setOptions(options);
	        this.parent(options);
	    },
	    build: function(){
	        var dim, yscroll, box, titleBar, closebutton, stagewrap, stagecontainer, stage;
	        dim = getScrollSize();
	        //check for fuggin IE people...
	        yScroll = self.pageYOffset ? self.pageYOffset : document.documentElement.scrollTop;
	        //primary container	
	        box = new Element('div', {
	            id:  'sjpad_base',
	            styles: {
	                position: 'absolute',
	                top: yScroll + 50, //the users eys tend to reside about 1/3 of the way down.
	                padding: '5px',
	                'z-index': this.baseIndex,
	                opacity: 0
	            },
	            events: {
	                dblclick: function(e){
	                    if (this.options.closeable) {
	                        this.hide();
	                        this.hideBox();
	                    }
	                }.bind(this)
	            }
	        });
	        if (this.options.className) {
	            box.addClass(this.options.className);
	        }		
	        titleBar = new Element('h2', {
				'class':'title draggable',
	            html: this.options.titleBar || ''
	        }).injectTop(box);
	        stagewrap = new Element('div', {
	            id: "stagewrap",
				'class':'bg-deep p_all-8'
	        }).inject(box);
	        stagecontainer = new Element('div', {
	            id: 'stagecontainer'
	        }).inject(stagewrap);
	        stage = new Element('div', {
	            id: 'stage',
				'class':'trans50 border-light pb-8'
	        }).inject(stagecontainer);
	        //inject everything into the 'box'
	        
	        // set the stage contents and save to object
	        stage.set('html', this.options.stage || '');
	        
	        this.setOptions({
	            stage: stage,
	            titleBar: titleBar,
	            modalBox: box,
	            closebutton: closebutton
	        });
	        box.inject(document.body);
	        box.setStyle('left', (dim.x / 2) - (box.getSize().x/1.5));
	        new Drag(box, {
	            handle: titleBar
	        });
	    },
	    showBox: function(options){
	        if (options) {
	            this.setOptions(options);
	        }
	        this.build();
	        this.reveal();
	        this.options.modalBox.fade('in');
			this.setOptions({isMaskOn:true});
			this.fireEvent('boxopen',null, 700);
	    },
	    hideBox: function(){
	        this.options.modalBox.fade('out');
	        this.hide();
	        this.options.modalBox.dispose();
			this.fireEvent('boxclose');
	    },
	    show: function(){
	        this.options.modalBox.fade('in');
			this.setOptions({isMaskOn:true});
	    }
	});
	SJPHOTO.GalleryBox = new Class({
		Extends:SJPHOTO.Overlay,
		Implements:[Options, Events],
		options:{
			_infoElement:null,
			physics:Fx.Transitions.Pow.easeOut,
			controlClass:'.controlFrame',
			displayEl:null,
			displaySelector:'description',
			datacells:null,
			autoShow:true,
			thumbs:[],
			lightsOn:false,
			lightControl:null,
			onComplete:$empty,
			onExif:$empty,
			onBeforeswap:$empty,
			onSwap:$empty,
			onImageload:$empty,
			onSelect:$empty,
			onUdate:$empty,
			onReady:$empty
		},
		initialize:function(options){
			if(options){
				this.setOptions(options);
			}
			this.parent({closeable: true});
			this.options.lightControl =$('lightControl');
			this.options.lightsOn = Cookie.read('lights');
			
			if(this.options.lightsOn == 'off'){
				this.lowerLights( true );
				Log.log('initial read', this.options.lightsOn)
			}else{
				this.raiseLights( true );
				Log.log('initial read', this.options.lightsOn)
			}
			
			
			this.options.datacells = $$('.exif');
			this.thumbs = $$('img[id^=thumb-]');
			this.element = $(this.options.displaySelector); 
			this.options._infoElement=$('img-info');
			if($defined(this.options.lightControl)){
				this.options.lightControl.addEvent('click', function(evt){
					evt.stop();
					var t=evt.target;
					switch (t.get('text')){
						case 'Lower Lights':
						this.lowerLights();
						break;
						
						case "Raise Lights":
						this.raiseLights();
						break;
						
						default:
						break;
					}
					//this.toggle();
				}.bind(this));
			}
			$$(this.options.controlClass).addEvents({
				mouseover:function(e){
					this.options._infoElement.reveal();
				}.bind(this)
			});		
					
			this.thumbs.fade('0.3');
			this.thumbs[0].fade('in').addClass('selected');
			if ($defined(this.options._infoElement)) {
				this.options._infoElement.dissolve();
				this.options._infoElement.addEvent('click', function(e){
					this.dissolve();
				});
			}
	
			this.thumbs.addEvents({
				mouseover:function(e){
					if (!e.target.hasClass('selected')) {
						e.target.fade('0.6');
					}
				},
				mouseout:function(e){
					if (!e.target.hasClass('selected')) {
						e.target.fade('0.3');
					}
				},
				/*
				 * the click function fades out and removes old image
				 * fetches the new image and fades it in.
				 * 
				 * new image is stored to reduce http reqest to 1 per thumbnail
				 * */
				click:function(e){
					e.stop();
					
					var thumb, link, newImg, oldImg, currentimg, fader;
					thumb = e.target;
					this.fireEvent('select', thumb);
					fader = this.element.getElement('img');
					//if we clicked the selected thumb - do nothing
					if(thumb.hasClass('selected')){return false;}
					
					//clear thumb classes and fade out
					this.thumbs.removeClass('selected');
					this.thumbs.fade('0.3');
	
					//fade select and fade in click thumb								
					thumb.fade('in');
					thumb.addClass('selected');				
					link = thumb.getParent().href;
					this.updateData(thumb);
					
					new Fx.Tween(fader,{
					    property:'opacity',
					    unit:'%',
						link:'chain',
						duration:'long',
						onComplete:function(evt){
							var newImg, oldImg;
							fader.dispose();
							oldImg = thumb.retrieve('image');
							if (!$defined(oldImg)) {
								this.loadingnew = true;
								newImg = new Asset.image(link, {
									 id:'display-img'
									,styles:{
										 visibility:'hidden'
										,opacity:0
									}
									,events:{
										load:function(evt, el){
											this.fireEvent('imageload', newImg)
											if (this.options.autoShow) {
												newImg.fade('in');
											}
										}.bind(this)
									}				 
								});
								thumb.store('image', newImg);
								newImg.inject(this.element,'bottom');						
							}else{
								loadingnew= false;
								oldImg.inject(this.element,'bottom').fade('in');
								this.fireEvent('imageload', oldImg)
							}// end if else		
							this.fireEvent('swap', $pick(newImg, oldImg));		

						}.bind(this)// end oncomplete
					}).start(0); //end tween
					
				}.bind(this)//end click event function
			});// end events declaration
			this.fireEvent('ready', [this.element, this.element.getElement('img')] );
		},
		
		/**
		 * Sets the Exif data from the image
		 * @method updateData
		 * @private
		 * @param {Object} thumb
		 */
		updateData:function(thumb){
			/**
			 * @type JSON: incoming exif data
			 * 
             * @property ( String ) 'imageModel'
             * @property ( Number ) 'focalLength'
             * @property ( String ) 'flash'
             * @property ( Number ) 'width' 
             * @property ( Number ) 'height'
            */
			var exif, cells, len;
			cells = this.options.datacells;
			if (!$defined(thumb.retrieve('exif'))) {
				new Request.JSON({
					method: 'get',
					url: thumb.getProperty('rel'),
					onSuccess:function(responseJSON, responseText){
						exif = responseJSON;
						thumb.store('exif', responseJSON);
						this.fireEvent('exif', responseJSON);
						var k = cells.length;
						while(k--){
							
							cells[k].set('text', exif[cells[k].id]);
						}						
					}.bind(this)
				}).send();
			}
			else {
				exif = thumb.retrieve('exif');
				this.fireEvent('exif', exif);
				var k = cells.length;
				while(k--){
					cells[k].set('text', exif[cells[k].id]);
				}			
			}				
		},
		
		/**
		 * returns the primary element
		 * @method toElement
		 * @return {HTMLElement}
		 */
		toElement:function(){
			return this.element;
		},
		
		/**
		 * hides a dark maks over the page at a z-index of 500
		 * also sets a cookie to remember if the lights are on/off
		 * 
		 * @method raiseLights
		 * @param pass  {Boolean} If true, function will skip animation 
		 * @return {GalleryBox} the class instance
		 */
		raiseLights:function( pass ){

			this.hide( pass );
			Cookie.write('lights','on',{path:'/'});
			if ($defined(this.options.lightControl)) {
				this.options.lightControl.set('text', 'Lower Lights');
			}
			return this;
		},
		
		/**
		 * Dims the lights of the page ( reveals a mask )
		 * @method lowerLights
		 * @param pass {Boolean} If set to true, animation of the mask will be skipped
		 * @param level {Decimal} the level to set the lights at, 1.0 = on, 0.0 = off
		 * @return {GalleryBox} The class instance
		 */
		lowerLights:function( pass, level ){

			this.reveal( pass, level );
			Cookie.write('lights','off',{path:'/'});
			if ($defined(this.options.lightControl)) {
				this.options.lightControl.set('text', 'Raise Lights');
			}
			return this;
		}
	});
	SJPHOTO.LoginHandler = new Class({
        Implements: [Options, Events],
        options: {
            selector: 'a[id^=ajaxlogin]',
            _elements: null,
            url: '/ajax/login/'
        },
        
        initialize: function(options){
            if (options) {
                this.setOptions(options);
            }
            this.options._elements = $$(this.options.selector);
            this.options._elements.addEvents({
				'click':function(e){
					e.stop();
					this.build();
				}.bind(this)
			});
        },// end initialize
		build:function(){
			var _url, pad, rhtml, subButton, canButton, regButton, adminli, login_set, login_form, that;
			_url = this.options.url;
			that = this;
			rhtml = new Request.HTML({
				url:_url,
				method:'get',
				onSuccess:function(responseTree, responseEls, responseHTML, responseJS){
					pad = new SJPHOTO.LaunchPad({
						titleBar:'Log In',
						stage:'',
						zindex:that.options.zindex
						
					});// end onSuccess
					
					subButton = new Element('a',{
						'class':'dark_button p_all-4',
						text:'log in',
						events:{
							click:function(evt){
								Log.log('click!');	
								var sHtml = new Request.JSON({
									url:_url,
									method:'post',
									data : 'username=' + $('id_username').value + "&password=" + $('id_password').value,
		                            onSuccess: function(token){
		                                if (token.user) {
		                                    pad.hideBox();
		                                    if (token.location) {
		                                        window.location = token.location;
		                                    }
		                                }
		                                else {
		                                    if (token.msg) {
		                                        var message = new Element('div', {
		                                            'id': 'message',
		                                            'text': token.msg,
		                                            'class': 'red align-c bold'
		                                        });
		                                        message.inject('stage', 'bottom');
		                                    }
		                                }
		                            }									
								}).send();
							}
						}
					});//end submit button
					
					canButton = new Element('a',{
						'class':'p_all-4 dark_button',
						text:'cancel',
						events:{
							'click':function(evt){
								evt.stop();
								pad.hideBox();
							}
						}
					});// end cancel button
					regButton = new Element('a',{
						'class':'p_all-4 dark_button',
						text:'register',
						href:'/users/register/'
					});
					login_form = new Element('form',{
						id:'login_form',
						action:_url,
						method:'post',
						events:{
							'keypress':function(e){
								if(e.key == 'enter'){
									e.stop();
									subButton.fireEvent('click', e.target);
								}
							}
						}
					});// end form definition
					
					
					pad.showBox();
					$('stage').adopt(login_form);										
					login_set = new Element('fieldset',{id:'login_set'}).inject(login_form);
					login_set.set('html', responseHTML);
					adminli = new Element('li').inject(login_set,'bottom');
					subButton.inject(adminli);
					regButton.inject(adminli);
					canButton.inject(adminli);
				}
			}).send();// end request
		}// end build		
	});//end loginhandler
	
	SJPHOTO.EditMode = new Class({
        Implements: [Options, Events],
        options: {
            isEditModeOn: false,
            editorScriptsLoaded: false,
            warningBlock: null,
			warningBlockColor:'#09F',
            MEDIA_URL: 'http://media.muskegohitmen.com/',
            formURL: null, //the url to retrive the editing form from
            editor_element: 'id_content', // the id of the textarea we are going to convert to the editor
            editorActions: "h2 h4 p | bold italic | insertunorderedlist indent outdent | undo redo | unlink | image | insertcode toggleview",
            wikiArea: 'js-wiki-',
            _RTE: null
            /* onBuildcomplete:$empty */
        },
        initialize: function(options){
            if (options !== undefined) {
                this.setOptions(options);
            }
            this.build();
            
        },
        build: function(){
            var block, close_btn, title, button_wrap;
            block = new Element('div', {
                id: 'warningBlock',
                styles: {
                    background: this.options.warningBlockColor,
                    padding: '10px 0px',
                    position: 'fixed',
                    bottom: '0',
                    'z-index': 10000,
                    opacity: 0,
                    visibility: 'hidden',
                    width: '100%'
                }
            }).addClass('width100').inject(document.body);
            title = new Element('h1', {
                'text': "Edit Mode",
                styles: {
                    'margin-right': '20px',
                    'color': '#000',
                    'font-family': "Arial Black"
                }
            });
            title.addClass('fr');
            button_wrap = new Element('span', {
                'class': 'fr mt-8 mr-10'
            }).inject(block);
            close_btn = new Element('a', {
                'class': 'dark_button',
                text: 'cancel!',
                events: {
                    'click': function(evt){
                        //console.log('click');
                        this.confirmExit();
                    }.bind(this)
                }
            }).inject(button_wrap);
            title.inject(block);
            this.setOptions({
                warningBlock: block
            });
        },
        confirmExit: function(){
            if (confirm("Are you sure you want to exit with out saving??")) {
                this.options.warningBlock.fade('out');
                this.turnOff.delay(800, this);
            }
        },
        turnOn: function(){
            if (!this.options.isEditModeOn) {
                this.setOptions({
                    isEditModeOn: true
                });
                this.options.warningBlock.fade('in');
            }
            else {
                return false;
            }
        },
        turnOff: function(){
            if (this.options.isEditModeOn) {
                this.setOptions({
                    isEditModeOn: false
                });
                
                window.location.reload();
            }
            else {
                return false;
            }
        },
        buildEditor: function(){
            if (!this.options.isEditModeOn) {
                this.turnOn();
            }
            else {
                return false;
            }
            var send_btn, form_wrap, form, moo, form_set, controls, csrf;
            
            form = new Element('form', {
                method: 'post',
                action: this.options.formURL,
                id: 'document_form',
                enctype: 'multipart/form-data'
            });
            form_set = new Element('fieldset', {}).inject(form);
            form_wrap = new Element('ul').inject(form_set);
            csrf = new Element('input',{
            	type:"hidden",
            	name:"csrfmiddlewaretoken",
            	"value":Cookie.read('csrftoken')
            }).inject( form )
            if (this.options.formURL === null) {
                return false;
            }
            
            new Request.HTML({
                method: 'get',
                url: this.options.formURL,
                onFailure: function(){
                	Log.log('fail');
                },
				onComplete:function(){
					Log.log('complete');
				},
                onSuccess: function(rTree, rEls, rHTML, rScripts){
                    var wikiContainer;
					Log.log('success');
                    wikiContainer = $$('div[id^={wikiArea}]'.substitute(this.options))[0];
                    wikiContainer.empty();
                    wikiContainer.adopt(form);
                    form_wrap.set('html', rHTML);
                    moo = $(this.options.editor_element).mooEditable({
                        externalCSS: "{MEDIA_URL}css/sjeditor.css".substitute(this.options),
                        actions: this.options.editorActions
                    });
                    this.options._RTE = moo;
					
					this.fireEvent('buildcomplete', this, 500);
                }.bind(this)
            }).send();
            
            controls = new Element('li').inject(form_set, 'bottom');
            send_btn = new Element('a', {
                text: "submit",
                href: "#",
                'class': 'dark_button p_all-6',
                events: {
                    'click': function(evt){
                        this.options._RTE.saveContent();
                        form.submit();
                    }.bind(this)
                }
            }).inject(controls);
            //this.fireEvent('buildcomplete',this, 800);
        },
        insert: function(content){
            this.options._RTE.selection.insertContent(content);
        }
    });
	SJPHOTO.MultiLineAutoComplete = new Class({
		Extends:Autocompleter.Request.JSON,
		Impliments:[Options, Events, Class.Occlude],
		options:{
			/*
			onRemove:$empty,
			onInsert:$empty,
			*/
			searchInput:null,
			mainInput:null,
			replaceInput:true,
			replaceID:'id_recipient',
			searchFieldID:'id_search',
			formID:'messageForm',
			optionClass:'selectbox-option',
			closeLinkClass:'small red',
			closeLinkHref:'#',
			highlightColor:'#09F',
			_inputdata:null,
			//autocompleter options
			tokens:null,
			postVar:'q',
			url:null,
			method:'POST'
			
		},
		initialize:function(options){
			if (options) {
				this.setOptions(options);
			}
			this.options.mainInput = $(this.options.searchFieldID);	
			this.options._inputdata= $(this.options.replaceID);
			this.options._inputdata.setProperty('type', 'hidden');
			this.parent(this.options.searchFieldID, this.options.url, this.options);
			var container = new Element('div',{
				'class':'multi-input'
			}).inject(this.options._inputdata,'before').adopt(this.options.mainInput);
			this.options.mainInput.focus();
			new Element('br',{
				'class':'clearfloat'
			}).inject(container,'bottom');
		},
		
		choiceSelect: function(choice) {
			if (choice) {
				this.choiceOver(choice);
			}
			this.setSelection(true);
			this.queryValue = false;
			this.hideChoices();
			// if we can't find a similar element in the list
			// make the new element and add to list
			if (!this.checkOptions({obj_id:choice.retrieve('obj_id')})) {
				var opt = new Element('li', {
					html: choice.get('text'),
					'class':'multiline '+ this.options.optionClass,
					events:{
						mouseover:function(e){
							//clean up and mess from the .highlight() method
							e.target.removeProperty('style');
						}
					}
				});
				new Element('a',{
					text:' (x)',
					'class':this.options.closeLinkClass,
					href:"#",
					events:{
						'click':function(e){
							e.target.getParent('li').dispose();
							this.options.mainInput.focus();
							this.fireEvent('remove');
						}.bind(this)
					}
				}).inject(opt);
				new Element('input',{
					type:'hidden',
					id:'data-'+choice.retrieve('obj_id')
				}).setProperties({
					'content_type':choice.retrieve('ct'),
					'obj_id':choice.retrieve('obj_id'),
					'value':choice.retrieve('username')
					}).inject(opt);
				opt.inject(this.options.mainInput, 'before');
				this.fireEvent('insert', opt);
			}
			//if we did find a similar element we don't do anything
			this.options.mainInput.value='';
		},
		checkOptions:function(opts){
			var options = $$('input[obj_id={obj_id}]'.substitute(opts)).getParent();
			if(options.length > 0){
				options[0].highlight(this.options.highlightColor);
				return true;
			}else{
				return false;
			}				 
		},
		setData:function(){
			data = $$('input[id^=data-]');
			var x = [];
			data.each(function(el){
				x.push(el.value);
			});
			this.options._inputdata.value = x.toString();
			x = null;
		}			
	});
window.SJPHOTO = SJPHOTO;
})(window);
window.addEvent('domready', function(e){
	new MenuMatic();
	new SJPHOTO.LoginHandler({
		zindex:1000
	});
	new Fx.SmoothScroll({
		links:'.smooth'
	})
});
