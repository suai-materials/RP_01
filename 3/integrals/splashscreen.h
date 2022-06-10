#ifndef SPLASHSCREEN_H
#define SPLASHSCREEN_H

#include <QNetworkReply>
#include <QObject>
#include <qqml.h>


class SplashScreen : public QObject
{
    Q_OBJECT
public:
    SplashScreen(QObject *parent = nullptr);
    void replyFinished(QNetworkReply *reply);
    QObject *loader;

signals:

};

#endif // SPLASHSCREEN_H
