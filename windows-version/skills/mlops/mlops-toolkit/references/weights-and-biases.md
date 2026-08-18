# Weights & Biases — ML Experiment Tracking

Track ML experiments, hyperparameter sweeps, model registry, and dashboards.

## Install

```bash
pip install wandb
wandb login
```

## Quick start

```python
import wandb

run = wandb.init(project="my-project", config={
    "learning_rate": 0.001, "epochs": 10, "batch_size": 32
})

for epoch in range(run.config.epochs):
    train_loss = train_epoch()
    wandb.log({"epoch": epoch, "train/loss": train_loss})

wandb.finish()
```

## PyTorch integration

```python
import wandb
wandb.init(project="pytorch-demo", config={"lr": 0.001, "epochs": 10})

for epoch in range(wandb.config.epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
            wandb.log({"loss": loss.item(), "epoch": epoch})

wandb.finish()
```

## Hyperparameter sweeps

```python
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {'name': 'val/accuracy', 'goal': 'maximize'},
    'parameters': {
        'learning_rate': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1},
        'batch_size': {'values': [16, 32, 64, 128]},
        'optimizer': {'values': ['adam', 'sgd', 'rmsprop']},
    }
}

sweep_id = wandb.sweep(sweep_config, project="my-project")

def train():
    run = wandb.init()
    lr = wandb.config.learning_rate
    # ... training loop ...
    wandb.log({"val/accuracy": val_acc})

wandb.agent(sweep_id, function=train, count=50)
```

## Artifacts (model versioning)

```python
# Log model
artifact = wandb.Artifact('model', type='model')
artifact.add_file('checkpoint.pth')
wandb.log_artifact(artifact)

# Download artifact
artifact = run.use_artifact('training-dataset:latest')
artifact_dir = artifact.download()
```

## Model registry

```python
model_artifact = wandb.Artifact('resnet50-model', type='model',
    metadata={'architecture': 'ResNet50', 'accuracy': 0.95})
model_artifact.add_file('model.pth')
wandb.log_artifact(model_artifact, aliases=['best', 'production'])
run.link_artifact(model_artifact, 'model-registry/production-models')
```

## Framework integrations

### HuggingFace Transformers
```python
training_args = TrainingArguments(report_to="wandb", run_name="bert-finetuning")
```

### PyTorch Lightning
```python
from pytorch_lightning.loggers import WandbLogger
wandb_logger = WandbLogger(project="lightning-demo", log_model=True)
trainer = Trainer(logger=wandb_logger, max_epochs=10)
```

### Keras/TensorFlow
```python
from wandb.keras import WandbCallback
model.fit(x_train, y_train, callbacks=[WandbCallback()])
```

## Best practices

- Use descriptive run names: `bert-base-lr0.001-bs32-epoch10`
- Organize with tags and groups
- Log system metrics (GPU util, memory)
- Save important artifacts
- Use offline mode for unstable connections: `os.environ["WANDB_MODE"] = "offline"`

## Pricing

- Free: Unlimited public projects, 100GB storage
- Academic: Free for students/researchers
- Teams: $50/seat/month

## Resources
- Docs: https://docs.wandb.ai
- GitHub: https://github.com/wandb/wandb
