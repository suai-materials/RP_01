#ifndef LOADERMANAGER_H
#define LOADERMANAGER_H

#include <QNetworkAccessManager>
#include <QObject>
#include <QQmlComponent>

enum Screen{
    Splash,
    Auth,
    Tests,
    Topics,
    Account
};

class LoaderManager : public QObject
{
    Q_OBJECT
public:
    explicit LoaderManager(QObject *parent = nullptr);
    Q_INVOKABLE QQmlComponent *getFrame(QObject *parent);
    void changeScreen(Screen screen);
    void replyFinished(QNetworkReply *reply);
signals:

private:
    QObject* loader;
    Screen screenNow;
    // QQmlComponent *frameNow = nullptr;
    QNetworkAccessManager *manager = new QNetworkAccessManager();
};

#endif // LOADERMANAGER_H
