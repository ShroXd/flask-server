node {
    stage('Git Pull') {
        git 'https://github.com/ShroXd/flask-server.git'
    }

    stage('Build Image') {
        try {
            sh 'docker stop novelser'
            sh 'docker rm novelser'
            sh 'docker rmi novelser'
        }
        catch (exc) {
            echo '无需清理容器残余'
        }
        finally {
            sh 'docker build -t novelser:latest .'
        }
    }

    stage('Deploy') {
        try {
          sh 'docker run -p 3000:5000 --name novelser -d novelser'
        }
        catch (exc) {
          echo '运行容器失败'
          sh 'docker stop novelser'
          sh 'docker rm novelser'
          sh 'docker run -p 3000:5000 --name novelser -d novelser'
        }
    }

}