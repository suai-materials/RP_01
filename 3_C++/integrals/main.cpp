#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include <QLocale>
#include <QTranslator>
#include <QObject>
#include <QtWebEngine/qtwebengineglobal.h>

#include <loadermanager.h>

static QObject *qobject_singletontype_provider(QQmlEngine *engine, QJSEngine *scriptEngine)
{
    Q_UNUSED(engine)
    Q_UNUSED(scriptEngine)
    static LoaderManager *loaderManager = new LoaderManager();
    return loaderManager;
}

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    // qmlRegisterType<SplashScreen>("com.integrals.splashscreen", 1, 0, "SplashScreen");
    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "integrals_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            app.installTranslator(&translator);
            break;
        }
    }
    qmlRegisterSingletonType<LoaderManager>("com.integrals.api", 1, 0, "LoaderManager", &qobject_singletontype_provider);
    QtWebEngine::initialize();
    QQmlApplicationEngine engine;
    const QUrl url(u"qrc:/integrals/main.qml"_qs);
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}
