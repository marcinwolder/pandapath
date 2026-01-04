import { Injectable } from '@angular/core';
import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import { ServiceStatusService } from './service-status.service';

@Injectable()
export class BackendStatusInterceptor implements HttpInterceptor {
  private backendOrigin = new URL(environment.backendHost).origin;

  constructor(private serviceStatus: ServiceStatusService) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    let requestOrigin: string | null = null;
    try {
      requestOrigin = new URL(req.url).origin;
    } catch {
      requestOrigin = null;
    }

    return next.handle(req).pipe(
      tap({
        next: () => {
          if (requestOrigin === this.backendOrigin) {
            this.serviceStatus.markBackendOnline();
          }
        },
        error: (error) => {
          if (
            requestOrigin === this.backendOrigin &&
            error instanceof HttpErrorResponse &&
            error.status === 0
          ) {
            this.serviceStatus.markBackendOffline();
          }
        }
      })
    );
  }
}
