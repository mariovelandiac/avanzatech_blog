import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { httpInterceptorProviders } from './interceptors/provider.interceptor';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    importProvidersFrom(HttpClientModule),
    httpInterceptorProviders, provideAnimationsAsync(), provideAnimationsAsync(), provideAnimationsAsync()
  ]
};
