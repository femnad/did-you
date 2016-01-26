@0xdff0d7a81f869f88;

struct Task {
    name @0 :Text;
}

struct TaskList {
    tasks @0: List(Task);
}

struct TaskMessage {

    task @0 :Task;
    command @1 :Command;

    enum Command {
        do @0;
        done @1;
    }

}
