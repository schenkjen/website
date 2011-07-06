/*
Script: MooEditable.Extras.js
	Extends MooEditable to include more (simple) toolbar buttons.

License:
	MIT-style license.
*/

MooEditable.Actions.extend({

	formatBlock: {
		title: 'Block Formatting',
		type: 'menu-list',
		options: {
			list: [
				{text: 'Paragraph', value: 'p'},
				{text: 'Heading 1', value: 'h1'},
				{text: 'Heading 2', value: 'h2'},
				{text: 'Heading 3', value: 'h3'}
			]
		},
		states: {
			tags: ['p', 'h1', 'h2', 'h3']
		},
		command: function(menulist, name){
			var argument = '<' + name + '>';
			this.execute('formatBlock', false, argument);
			this.focus();
		}
	},
	
	justifyleft:{
		title: 'Align Left',
		states: {
			css: {'text-align': 'left'}
		}
	},
	
	justifyright:{
		title: 'Align Right',
		states: {
			css: {'text-align': 'right'}
		}
	},
	
	justifycenter:{
		title: 'Align Center',
		states: {
			tags: ['center'],
			css: {'text-align': 'center'}
		}
	},
	
	justifyfull:{
		title: 'Align Justify',
		states: {
			css: {'text-align': 'justify'}
		}
	},
	h4: {
		title: 'H4',
		states: {
			tags: ['h4']
		},
		command: function(name){
			var argument = '<' + 'h4' + '>';
			this.execute('formatBlock', false, argument);
		}
	},
	h3: {
		title: 'H3',
		states: {
			tags: ['h3']
		},
		command: function(name){
			var argument = '<' + 'h3' + '>';
			this.execute('formatBlock', false, argument);
		}
	},
	
	h2: {
		title: 'H2',
		states: {
			tags: ['h2']
		},
		command: function(name){
			var argument = '<' + 'h2' + '>';
			this.execute('formatBlock', false, argument);
		}
	},
	p:{
		title:'Paragragh',
		type:'button',
		options: {
			states: {
				tags: ['p']
			},
			mode:'icon'
		},
		command: function(name){
			var argument = '<' + name.name + '>';
			this.focus();
			this.execute('formatBlock', false, argument);
		}
	}
});
