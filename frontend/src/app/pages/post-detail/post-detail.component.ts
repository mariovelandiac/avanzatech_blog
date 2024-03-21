import { Component, OnInit } from '@angular/core';
import { PostTitleTeamUserComponent } from '../../components/post-title-team-user/post-title-team-user.component';
import { PostService } from '../../services/post.service';
import { LikeService } from '../../services/like.service';
import { CommentService } from '../../services/comment.service';
import { AuthService } from '../../services/auth.service';
import { ActivatedRoute } from '@angular/router';
import { PostRetrieve } from '../../models/interfaces/post.interface';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-post-detail',
  standalone: true,
  imports: [PostTitleTeamUserComponent, CommonModule],
  templateUrl: './post-detail.component.html',
  styleUrl: './post-detail.component.sass'
})
export class PostDetailComponent implements OnInit {
  isAuthenticated = false;
  postId!: number;
  post: PostRetrieve | undefined;
  initialCommentIndexPage = 0;

  constructor(
    private postService: PostService,
    private likeService: LikeService,
    private commentService: CommentService,
    private authService: AuthService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.authService.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
    this.route.paramMap.subscribe((params) => {
      this.postId = +params.get('id')!;
      this.fetchData();
    });
  };

  fetchData() {
    this.postService.retrieve(this.postId).subscribe((post) => {
      this.post = post;
    });
  }
}
