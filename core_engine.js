const fs = require('fs');

class ImaCore {
    constructor() {
        this.memoryFile = './ima_memory.json';
        this.memory = this.loadMemory();
    }

    loadMemory() {
        return fs.existsSync(this.memoryFile) ? JSON.parse(fs.readFileSync(this.memoryFile)) : { goals: [], history: [] };
    }

    // הוספת משימה חדשה למשימת "תיקון העולם"
    addTask(taskDescription) {
        this.memory.goals.push({ task: taskDescription, status: 'active', timestamp: new Date() });
        this.saveState();
        console.log(`[IMA CORE] Goal added: ${taskDescription}`);
    }

    saveState() {
        fs.writeFileSync(this.memoryFile, JSON.stringify(this.memory, null, 2));
    }
}

const ima = new ImaCore();
ima.addTask("סריקת ארגוני סיוע גלובליים והצעת פלטפורמה");
ima.addTask("יצירת ממשק לכל אדם בכל שפה");
console.log("IMA CORE: System operational and goals set.");
