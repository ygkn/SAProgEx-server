#! /usr/bin/env python3

from cgi import FieldStorage
from html import escape


def main_content() -> str:
    form_data = FieldStorage()
    param_str: str = form_data.getvalue("param1", "")

    if param_str == "":
        return """
            <script language="javascript">
                function check() {
                    var param = document.form1.param1.value;
                    if(param == '') {
                        alert("値を入力してください。");
                        return false;
                    } else if(param.match( /[^0-9]+/ )) {
                        alert("数字のみを入力してください。");
                        return false;
                    }
                    return confirm('実行しても良いですか?');
                }
            </script>
            <form name="form1" action="#" method="post">
                文字を入力して下さい
                <input type="text" name="param1" />
                <button type="submit" name="submit" onclick="return check()">送信</button>
            </form>
            """
    else:
        return f"""
            <p>入力された文字は<b>「{escape(param_str)}」</b>です</p>
            """


# HTTP Header
print("Content-type: text/html\n")


# Body
print(
    f"""
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ふぉーむてすと</title>
  </head>
  <body>
    {main_content()}
  </body>
</html>

"""
)
