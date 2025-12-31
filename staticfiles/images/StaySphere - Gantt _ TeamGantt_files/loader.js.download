const root = document.getElementById('root');
if (root) {
  root.innerHTML = `
  <style>
    @keyframes loader-animation {
      0% {
        opacity: 1;
        transform: scale(1);
      }

      100% {
        opacity: 0.75;
        transform: scale(0.95);
      }
    }

    html, body {
      height: 100%;
    }

    body {
      align-items: center;
      display: flex;
      justify-content: center;
      margin: auto;
    }

    .loader svg {
      animation: loader-animation 0.8s
          cubic-bezier(0.53, 0.22, 0.85, 0.58) 0s infinite alternate;
      display: block;
      fill: #888a8c;
      height: 48px;
      margin: 0 auto;
      width: 48px;
    }

  </style>
  <div class="loader">
    <svg height="100%" viewBox="0 0 26 26" width="100%">
      <g>
        <path d="M25.728 5.119H.208A.213.213 0 0 1 0 4.903V.453C0 .336.093.238.207.238h25.52c.115 0 .208.098.208.217v4.449a.213.213 0 0 1-.207.216 M25.732 12.224H6.686a.208.208 0 0 1-.202-.211V7.519c0-.117.091-.212.202-.212h19.046c.112 0 .203.095.203.212v4.494a.208.208 0 0 1-.203.211M25.74 19.157H13.163a.199.199 0 0 1-.195-.202v-4.4c0-.11.088-.202.195-.202H25.74c.106 0 .194.091.194.203v4.399z" />
      </g>
    </svg>
  </div>
  `;
}
