NECESSARIA_module.declare([], function(r, e){
	var Switch = function(){
		this.on = false;
		this.onswitchon = function(){};
		this.onswitchoff = function(){};
	}
	Switch.prototype.turn = function(act){
		if(arguments.length)
			this.on = act
		else
			this.on = !this.on;
		if(this.on){
			this.onswitchon()
		} else {
			this.onswitchoff()
		}
	};
	e.Switch = Switch;
});
