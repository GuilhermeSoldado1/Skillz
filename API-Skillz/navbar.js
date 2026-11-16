function renderNavbar() {
     let txt = `
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="#">marca</a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="menu">
                            <ul class="navbar-nav me-auto">
                                <li class="nav-item"><a class="nav-link active" href="#">lista</a></li>
                                <li class="nav-item"><a class="nav-link" href="#">link1</a></li>
                                <li class="nav-item"><a class="nav-link" href="#">link2</a></li>
                            </ul>
                        </div>
                    </div>
                </nav>
            `;
            $('#navbar').html(txt)
}

$(function(){
    renderNavbar
})