function main() {
  const bookmarkData = JSON.parse(document.getElementById('bookmark-data').innerHTML);
  const bookmarkContainer = document.getElementById('bookmark-container');

  const bookmarkDomList = bookmarkData.map((data) => {
    const dom = document.createElement('li');
    const title = data.title || data.url;
    dom.innerHTML = `<a href="${data.url}">${title}</a>`;
    return dom;
  });

  bookmarkDomList.forEach((li) => { bookmarkContainer.appendChild(li) });
}

document.addEventListener('DOMContentLoaded', main);
