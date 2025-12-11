from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(error):
    return (
        render_template(
            "error.html",
            title="Страница не найдена (404)",
            message="Запрошенная страница не существует или была перемещена.",
            image="error-404.png",
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "error.html",
            title="Внутренняя ошибка сервера (500)",
            message="Произошла непредвиденная ошибка. Попробуйте обновить страницу или вернуться позже.",
            image="error-500.png",
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
