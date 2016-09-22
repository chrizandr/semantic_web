/*
jQWidgets v4.2.1 (2016-Aug)
Copyright (c) 2011-2016 jQWidgets.
License: http://jqwidgets.com/license/
*/

(function(a){a.jqx.jqxWidget("jqxPopover","",{});a.extend(a.jqx._jqxPopover.prototype,{defineInstance:function(){var b={arrowOffsetValue:null,animationType:"fade",position:"bottom",animationOpenDelay:"fast",animationCloseDelay:"fast",autoClose:true,isModal:false,height:null,initContent:null,offset:null,rtl:false,showArrow:true,showCloseButton:false,selector:null,title:"",width:null,_toggleElement:null,_popover:null,_popoverTop:0,_popoverLeft:0,_init:false,_ie8:(a.jqx.browser.msie&&a.jqx.browser.version===8),_ie7:(a.jqx.browser.msie&&a.jqx.browser.version<8),_left:0,_top:0,events:["open","close"]};a.extend(true,this,b);return b},createInstance:function(){var b=this;b._content=b.host.children()},render:function(){var h=this;var c=h.element.id;h._content.detach();h._toggleElement=a(h.selector);if(h._toggleElement.length===0){throw new Error('jqxPopover: Invalid Popover toggler: "'+h.selector+'".')}else{if(h._toggleElement===null){throw new Error("jqxPopover: Missing Popover toggler.")}}var k=a('<div id="'+c+'" class="'+h.toThemeProperty("jqx-popover")+'"><div class="'+h.toThemeProperty("jqx-popover-arrow")+'"></div><div class="'+h.toThemeProperty("jqx-popover-title")+'"></div><div class="'+h.toThemeProperty("jqx-popover-content")+'"></div></div>');a("body").append(k);var g=h.host.data();h.host.detach();h.host=k;h.host.data(g);h.element=k[0];h.element.id=c;h._popover=a("#"+c);var j=h._popover.find(".jqx-popover-title");j.append(h.title);var i=h._popover.find(".jqx-popover-content");i.append(h._content);h._popover.hide();h._removeHandlers();h._addHandlers();h._popover.addClass(h.position);j.addClass(h.toThemeProperty("jqx-widget-header"));h._popover.addClass(h.toThemeProperty("jqx-widget jqx-widget-content jqx-rc-all"));if(h.showArrow){h._popover.addClass(h.toThemeProperty("jqx-popover-arrow-"+h.position))}if(h.rtl){j.addClass(h.toThemeProperty("jqx-rtl"));j.css("direction","rtl");i.css("direction","rtl")}if(h.showCloseButton){var d=a('<div class="'+this.toThemeProperty("jqx-window-close-button-background")+'"></div>');var e=a('<div style="width: 100%; height: 100%;" class="'+this.toThemeProperty("jqx-window-close-button")+" "+this.toThemeProperty("jqx-icon-close")+'"></div>');d.append(e);j.append(d);j.css("min-height","16px");d.addClass(h.toThemeProperty("jqx-popover-close-button"));h.closeButton=e;if(h.rtl){d.addClass(h.toThemeProperty("jqx-popover-close-button-rtl"))}}if(h.arrowOffsetValue){if(h.position=="bottom"||h.position=="top"){var b=h._popover.find(".jqx-popover-arrow").css("margin-left");h._popover.find(".jqx-popover-arrow").css("margin-left",parseInt(b)+h.arrowOffsetValue)}else{var f=h._popover.find(".jqx-popover-arrow").css("margin-top");h._popover.find(".jqx-popover-arrow").css("margin-top",parseInt(f)+h.arrowOffsetValue)}}if(h.width||h.height){h._popover.css("width",h.width);h._popover.css("height",h.height)}},refresh:function(b){this.render()},destroy:function(){var b=this;if(b.length!==0){b._removeHandlers();b._popover.remove();b._removeModalBackground()}},propertyChangedHandler:function(b,c,f,e){var d=this;d.render()},_stickToToggleElement:function(){var g=this;g._popover.css("left","0px");g._popover.css("top","0px");var j=g._toggleElement;var e=j.offset();var b=j.outerHeight();var h=j.outerWidth();var d=g._popover.height();var i=g._popover.width();switch(g.position){case"left":g._popoverTop=e.top-d/2+b/2;g._popoverLeft=e.left-g._popover.outerWidth();break;case"right":g._popoverTop=e.top-d/2+b/2;g._popoverLeft=e.left+h;break;case"top":g._popoverTop=e.top-g._popover.outerHeight();g._popoverLeft=e.left-i/2+h/2;break;case"bottom":g._popoverTop=e.top+b;g._popoverLeft=e.left-i/2+h/2;break}var c=g.offset?g.offset.left:0;var f=g.offset?g.offset.top:0;g._popover.css("top",f+g._popoverTop);g._popover.css("left",c+g._popoverLeft)},open:function(){var c=this;c._stickToToggleElement();function d(){c._popover.show();c._raiseEvent("0");c._isOpen=true}function b(){if(c.initContent&&c._init===false){c.initContent();c._init=true;c._stickToToggleElement()}}if(c._ie7===true){d();b();return}switch(c.animationType){case"fade":c._popover.fadeIn(c.animationOpenDelay,function(){c._raiseEvent("0");b();c._isOpen=true});break;case"none":d();b();break}c._makeModalBackground()},close:function(){var c=this;if(!c._isOpen){return}function b(){c._popover.hide();c._raiseEvent("1");c._isOpen=false}if(c._ie7===true){b();return}switch(c.animationType){case"fade":c._popover.fadeOut(c.animationCloseDelay,function(){c._raiseEvent("1");c._isOpen=false});break;case"none":b();break}c._removeModalBackground()},_raiseEvent:function(f,c){if(c===undefined){c={owner:null}}var d=this.events[f];c.owner=this;var e=new a.Event(d);e.owner=this;e.args=c;if(e.preventDefault){e.preventDefault()}var b=this._popover.trigger(e);return b},_makeModalBackground:function(){var b=this;if(b.isModal===true){b.modalBackground=a("<div></div>");b.modalBackground.addClass(this.toThemeProperty("jqx-popover-modal-background"));a(document.body).prepend(b.modalBackground);a(document.body).addClass(b.toThemeProperty("jqx-unselectable"));b.host.addClass(b.toThemeProperty("jqx-selectable"))}},_removeModalBackground:function(){var b=this;if((b.isModal===true)&&(b.modalBackground!==undefined)){b.modalBackground.remove();a(document.body).removeClass(b.toThemeProperty("jqx-unselectable"));b.host.removeClass(b.toThemeProperty("jqx-selectable"))}},_addHandlers:function(){var b=this,c=b.element.id;b.addHandler(a(document),"keydown.jqxPopover"+c,function(d){if(d.keyCode==27){b.close()}});b.addHandler(a(document),"click.jqxPopover"+c,function(d){if(b.closeButton&&d.target==b.closeButton[0]){b.close()}if(b.autoClose===true){if(d.target!=b.element&&!a(d.target).ischildof(b._popover)){if(!b.isModal){b.close()}}}});b.addHandler(a(window),"resize.jqxPopover"+c,function(d){if(b.element.style.display!="none"){b._stickToToggleElement()}});if(b.selector){b.addHandler(b._toggleElement,"click.jqxPopover"+c,function(d){d.stopPropagation();if(b.host.css("display")!="none"){b.close()}else{b.open()}})}},_removeHandlers:function(){var b=this,c=b.element.id;b.removeHandler(a(document),"click.jqxPopover"+c);if(b.selector){b.removeHandler(b._toggleElement,"click.jqxPopover"+c)}b.removeHandler(a(document),"keydown.jqxPopover"+c);b.removeHandler(a(window),"resize.jqxPopover"+c)}})})(jqxBaseFramework);