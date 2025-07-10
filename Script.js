document.addEventListener("DOMContentLoaded", () => {
  const storedTasks = JSON.parse(localStorage.getItem("tasks"));

  if (storedTasks) {
    storedTasks.forEach((task) => tasks.push(task));
    updatetasklist();
    updateStats();
  }
});

let tasks = [];

const saveTask = () => {
  localStorage.setItem("tasks", JSON.stringify(tasks));
};

const addTask = () => {
  const Taskinput = document.getElementById("Taskinput");
  const text = Taskinput.value.trim();
  if (text) {
    tasks.push({ text: text, completed: false });
    Taskinput.value = "";
    updatetasklist();
    updateStats();
    saveTask();
  }
};

const toogleTaskComplete = (index) => {
  tasks[index].completed = !tasks[index].completed;
  updateStats();
  saveTask();
};

const updateStats = () => {
  const compeletetask = tasks.filter((task) => task.completed).length;
  const totaltask = tasks.length;
  const progress = (compeletetask / totaltask) * 100;
  const progressbar = document.getElementById("progress");

  progressbar.style.width = ` ${progress}%`;
  document.getElementById(
    "numbers"
  ).innerText = ` ${compeletetask}/${totaltask}`;
  if (tasks.length && compeletetask === totaltask) {
    Animations();
  }
};

const deletetask = (index) => {
  tasks.splice(index, 1);
  updatetasklist();
  updateStats();
  saveTask();
};

const editask = (index) => {
  const Taskinput = document.getElementById("Taskinput");
  Taskinput.value = tasks[index].text;

  tasks.splice(index, 1);
  updatetasklist();
  updateStats();
  saveTask();
};

const updatetasklist = () => {
  const tasklist = document.getElementById("tasklist");
  tasklist.innerHTML = "";

  tasks.forEach((task, index) => {
    const listitems = document.createElement("li");
    listitems.innerHTML = `
    <div class="taskitem ">
        <div class="task ${task.completed ? "completed" : ""} ">
            <input type="checkbox" class="checkbox" ${
              task.completed ? "checked" : ""
            } >
            <p> ${task.text} </p>
        </div>
        <div class="icons">
            <img src="./edit.png" onClick="editask(${index})" >
            <img src="./delete.png" onClick="deletetask(${index})">
        </div>
    </div>
`;
    listitems.addEventListener("change", () => toogleTaskComplete(index));
    tasklist.append(listitems);
  });
};

document.getElementById("newTask").addEventListener("click", (e) => {
  e.preventDefault();

  addTask();
});

const Animations = () => {
  const count = 200,
    defaults = {
      origin: { y: 0.7 },
    };

  function fire(particleRatio, opts) {
    confetti(
      Object.assign({}, defaults, opts, {
        particleCount: Math.floor(count * particleRatio),
      })
    );
  }

  fire(0.25, {
    spread: 26,
    startVelocity: 55,
  });

  fire(0.2, {
    spread: 60,
  });

  fire(0.35, {
    spread: 100,
    decay: 0.91,
    scalar: 0.8,
  });

  fire(0.1, {
    spread: 120,
    startVelocity: 25,
    decay: 0.92,
    scalar: 1.2,
  });

  fire(0.1, {
    spread: 120,
    startVelocity: 45,
  });
};
