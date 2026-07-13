class IMAEvents {
    constructor(){
        this.listeners={}
    }

    on(name,fn){
        if(!this.listeners[name])
            this.listeners[name]=[]
        this.listeners[name].push(fn)
    }

    emit(name,data){
        for(const fn of this.listeners[name]||[])
            fn(data)
    }
}

module.exports=new IMAEvents()
