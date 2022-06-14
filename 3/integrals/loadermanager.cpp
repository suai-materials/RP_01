#include "loadermanager.h"

#include <QNetworkReply>
#include <thread>
#include <chrono>

LoaderManager::LoaderManager(QObject *parent)
    : QObject{parent}
{
    connect(manager, &QNetworkAccessManager::finished, this, &LoaderManager::replyFinished);
    QNetworkRequest request;
    request.setUrl(QUrl("https://pank.su"));
    // Отправляем запрос на проверку интернет соединения
    manager->get(request);
}

QQmlComponent *LoaderManager::getFrame(QObject *parent) {
    QQmlEngine *engine = qmlEngine(parent);
    if (engine){
        //this->parent = parent;
        loader = parent->findChild<QObject *>("pageLoader");

    }
    return new QQmlComponent(engine, QUrl("qrc:/splash.qml"));;
}


void LoaderManager::replyFinished(QNetworkReply *reply){
    if (reply->error()) {
        qDebug() << reply->errorString();
        return;
    }
    QVariant statusCode = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute);
    if (statusCode.isValid() && statusCode.toInt() == 200){
        // Делаем вид пользователю, что у нас долгая загрузка
        std::this_thread::sleep_for(std::chrono::seconds(1));
        changeScreen(Auth);
    }
}

// меняем источник loader для смены текущего frame
void LoaderManager::changeScreen(Screen screen){
    switch (screen) {
        case Splash:
            loader->setProperty("source", "splash.qml");
            break;
        case Auth:
            loader->setProperty("source", "auth.qml");
            break;
        default:
            loader->setProperty("source", "splash.qml");
            break;
    }
}
