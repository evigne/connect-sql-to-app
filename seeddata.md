To create a PostgreSQL database in Kubernetes and seed it with your `seeddb.sql` file, you'll need to complete a few steps. Here’s a comprehensive guide on how to do this:

### 1. Create a PostgreSQL Deployment and Service

First, you need a PostgreSQL deployment and a service to expose it. Below is an example of a Kubernetes YAML file that creates both.

**postgres-deployment.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  ports:
  - port: 5432
  selector:
    app: postgres
  clusterIP: None
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  selector:
    matchLabels:
      app: postgres
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:latest
        env:
        - name: POSTGRES_DB
          value: mydatabase
        - name: POSTGRES_USER
          value: user
        - name: POSTGRES_PASSWORD
          value: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

### 2. Create a PersistentVolumeClaim

To store database data persistently, create a PersistentVolumeClaim (PVC). Here is an example:

**postgres-pvc.yaml**:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```

### 3. Create a ConfigMap for the SQL Seed File

Next, create a ConfigMap from your `seeddb.sql` file. This allows your Kubernetes pods to access the SQL script.

```bash
kubectl create configmap seed-script --from-file=seeddb.sql
```

### 4. Create a Job to Seed the Database

Finally, you can create a Kubernetes Job that will seed your database using the SQL file in the ConfigMap. Here is an example of a job configuration:

**postgres-seed-job.yaml**:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-seed
spec:
  template:
    spec:
      containers:
      - name: psql-seed
        image: postgres:latest
        command: ["psql"]
        args: ["-U", "user", "-d", "mydatabase", "-f", "/scripts/seeddb.sql"]
        env:
        - name: PGPASSWORD
          value: password
        volumeMounts:
        - name: scripts
          mountPath: /scripts
      restartPolicy: Never
      volumes:
      - name: scripts
        configMap:
          name: seed-script
```

### Steps to Deploy

1. **Apply the PersistentVolumeClaim**:
   ```bash
   kubectl apply -f postgres-pvc.yaml
   ```

2. **Deploy PostgreSQL**:
   ```bash
   kubectl apply -f postgres-deployment.yaml
   ```

3. **Seed the Database**:
   ```bash
   kubectl apply -f postgres-seed-job.yaml
   ```

This setup will deploy a PostgreSQL instance in your Kubernetes cluster and seed it using your SQL script. Modify the database credentials and adjust the storage requirements as necessary for your environment.