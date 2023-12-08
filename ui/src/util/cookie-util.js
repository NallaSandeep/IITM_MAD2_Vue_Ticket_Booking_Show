export function setCookie(name, value, minutesToExpire) {
  const expirationDate = new Date();
  expirationDate.setTime(
    expirationDate.getTime() + minutesToExpire * 60 * 1000
  ); // Convert minutes to milliseconds

  const cookieValue =
    encodeURIComponent(value) + "; expires=" + expirationDate.toUTCString();
  document.cookie = name + "=" + cookieValue;
}

export function deleteCookie(name) {
  const pastDate = new Date(0); // Set to a date in the past
  document.cookie = name + "=; expires=" + pastDate.toUTCString();
}

export function getCookie(name) {
  const cookieName = name + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookieArray = decodedCookie.split(";");

  for (let i = 0; i < cookieArray.length; i++) {
    let cookie = cookieArray[i];
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return null;
}
