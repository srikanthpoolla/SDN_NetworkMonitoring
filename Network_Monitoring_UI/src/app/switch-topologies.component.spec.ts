import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwitchTopologiesComponent } from './switch-topologies.component';

describe('SwitchTopologiesComponent', () => {
  let component: SwitchTopologiesComponent;
  let fixture: ComponentFixture<SwitchTopologiesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwitchTopologiesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwitchTopologiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
