#include "splashscreen.h"

SplashScreen::SplashScreen(QObject *parent){
    QNetworkAccessManager *manager = new QNetworkAccessManager();
    connect(manager, &QNetworkAccessManager::finished,
            this, &SplashScreen::replyFinished);

    manager->get(QNetworkRequest(QUrl("http://phhask.pank.su")));
}


void SplashScreen::replyFinished(QNetworkReply *reply){
    QVariant status_code = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute);
    if (status_code.isValid()){
        if (status_code.toInt() == 200){
          qmlContext(this)
        }
    }

//    QString answer = reply->readAll();
//    qDebug() << answer;
}
