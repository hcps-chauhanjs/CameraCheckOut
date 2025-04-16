/*Write the necessary code to replace the comment below*/

class LocalStorageManager {
    constructor(model, lsKey) {
        this.lsKey = lsKey;
        let existingValues = JSON.parse(localStorage.getItem(lsKey));
        if(existingValues) {
            for (let val of existingValues) {
                model.addItem(val);
            }
        }
        
        model.subscribe(function(scope, msg) {
            if(msg === 'changedItems') {
                this.save(scope.getItems());
            }
        }.bind(this));
    }
    save(data) {
        localStorage.setItem(this.lsKey, JSON.stringify(data));
    }
    
}