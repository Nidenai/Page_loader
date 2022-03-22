window.addEventListener('load', () => {
    const desktopBrandBanner =  document.querySelector('#adfox_163212557655936480');
    if(desktopBrandBanner) {
        const outerInner = desktopBrandBanner.closest('.outer_inner');
        const outerOuter = desktopBrandBanner.closest('.outer_outer');
        const adfoxBannerBg = outerOuter.querySelector('.adfox-banner-background');

        if (adfoxBannerBg === null) {
            const blockWithHeight = outerInner.querySelector('div:first-of-type');
            blockWithHeight.style.height = 0;
        }
    }
})